import time, json
from machine import Pin
import config
from net_mqtt import wifi_connect, mqtt_connect
from controller import MotorHBridge, LineSensor, clamp

# ---------- Helpers ----------
def now_iso():
    # lightweight ISO-ish timestamp; logger also accepts plain ts strings
    t = time.time()
    return "{}".format(t)

def gen_run_id():
    # Stable + filesystem-safe
    # Example: 1700000000_R1
    return "{}_R1".format(int(time.time()))

def pressed(pin: Pin) -> bool:
    # buttons are typically pull-up -> pressed == 0
    return pin.value() == 0

# ---------- Segment "track memory" ----------
class Segmenter:
    """
    Builds a simple temporal topological map from steering output:
    STRAIGHT / LEFT / RIGHT / SHARP_LEFT / SHARP_RIGHT / LOST
    """
    def __init__(self):
        self.cur = None
        self.t0 = time.ticks_ms()
        self.items = []  # last N segments in RAM (also emit events to log permanently)

    def classify(self, steer: float, lost: bool):
        if lost:
            return "LOST"
        a = abs(steer)
        if a < 0.08:
            return "STRAIGHT"
        if steer < 0:
            return "SHARP_LEFT" if a > 0.35 else "LEFT"
        else:
            return "SHARP_RIGHT" if a > 0.35 else "RIGHT"

    def update(self, steer: float, lost: bool):
        typ = self.classify(steer, lost)
        if self.cur is None:
            self.cur = typ
            self.t0 = time.ticks_ms()
            return None

        if typ != self.cur:
            t1 = time.ticks_ms()
            seg = {
                "type": self.cur,
                "dur_ms": time.ticks_diff(t1, self.t0)
            }
            self.items.append(seg)
            # keep small in RAM
            if len(self.items) > 50:
                self.items.pop(0)
            self.cur = typ
            self.t0 = t1
            return seg
        return None

# ---------- Recovery logic ----------
class Recovery:
    def __init__(self):
        self.active = False
        self.stage = 0
        self.t_start = 0
        self.last_bias = "NONE"  # LEFT or RIGHT

    def start(self, bias: str):
        self.active = True
        self.stage = 0
        self.t_start = time.ticks_ms()
        self.last_bias = bias

    def stop(self):
        self.active = False

    def timed_out(self):
        return time.ticks_diff(time.ticks_ms(), self.t_start) > config.RECOVERY_TIMEOUT_MS

    def step(self, motorL, motorR):
        # Simple pattern:
        # 0) reverse short
        # 1) spin search (biased)
        # 2) pause
        elapsed = time.ticks_diff(time.ticks_ms(), self.t_start)

        if self.stage == 0:
            motorL.set(config.RECOVERY_REVERSE_SPEED)
            motorR.set(config.RECOVERY_REVERSE_SPEED)
            if elapsed > config.RECOVERY_REVERSE_MS:
                self.stage = 1
                self.t_start = time.ticks_ms()

        elif self.stage == 1:
            s = config.RECOVERY_SPIN_SPEED
            # bias spin direction based on last steering direction
            if self.last_bias == "LEFT":
                motorL.set(-s)
                motorR.set(+s)
            else:
                motorL.set(+s)
                motorR.set(-s)

            if elapsed > config.RECOVERY_SPIN_MS:
                self.stage = 2
                self.t_start = time.ticks_ms()

        else:
            motorL.set(0.0)
            motorR.set(0.0)
            # loop spin again
            if elapsed > 120:
                self.stage = 1
                self.t_start = time.ticks_ms()

# ---------- Setup hardware ----------
btn_start = Pin(config.BTN_START, Pin.IN, Pin.PULL_UP)  # GP20 :contentReference[oaicite:7]{index=7}
btn_cal   = Pin(config.BTN_CAL,   Pin.IN, Pin.PULL_UP)  # GP21 :contentReference[oaicite:8]{index=8}

motorL = MotorHBridge(config.M1A, config.M1B)  # GP8/9 :contentReference[oaicite:9]{index=9}
motorR = MotorHBridge(config.M2A, config.M2B)  # GP10/11 :contentReference[oaicite:10]{index=10}

sensor = LineSensor(config.LINE_ADC_PIN)

# ---------- Runtime state ----------
V_black = None
V_white = None
V_mid = None
run_id = None
seq = 0

segmenter = Segmenter()
recovery = Recovery()

# PD controller memory
last_err = 0.0
last_t = time.ticks_ms()

# Lost-line detection
lost_since = None

# ---------- Network ----------
mqtt = None

def mqtt_pub(topic: bytes, obj: dict):
    global mqtt
    if mqtt is None:
        return
    try:
        mqtt.publish(topic, json.dumps(obj))
    except Exception:
        # best effort; never crash control loop
        pass

def cmd_handler(topic, msg):
    """
    Later: PicoClaw bridge publishes to bocobot/cmd:
    Examples:
      {"action":"slowdown","base_speed":0.35,"duration_ms":3000}
      {"action":"set_gains","kp":0.8,"kd":0.05}
    """
    global last_err
    try:
        data = json.loads(msg)
    except Exception:
        return

    action = data.get("action")
    if action == "set_gains":
        kp = data.get("kp")
        kd = data.get("kd")
        if isinstance(kp, (int, float)):
            config.Kp = float(kp)
        if isinstance(kd, (int, float)):
            config.Kd = float(kd)

def mqtt_init():
    global mqtt
    wifi_connect(config.WIFI_SSID, config.WIFI_PASS)
    mqtt = mqtt_connect(client_id=config.ROBOT_ID, host=config.MQTT_HOST, port=config.MQTT_PORT)
    mqtt.set_callback(cmd_handler)
    mqtt.subscribe(config.TOPIC_CMD)

# ---------- Calibration ----------
def read_voltage_u16(u16):
    # For logging only; absolute volts not required for control
    return (u16 / 65535.0) * 3.3

def do_calibration():
    global V_black, V_white, V_mid
    # Simple guided calibration:
    # - press CAL to capture BLACK
    # - press CAL again to capture WHITE
    # (You can reverse order; just follow prompts in serial)
    print("[CAL] Place sensor on BLACK then press CAL button...")
    while pressed(btn_cal) is False:
        time.sleep(0.02)
    time.sleep(0.25)
    V_black = sensor.read_u16()

    print("[CAL] Place sensor on WHITE then press CAL button...")
    while pressed(btn_cal) is True:
        time.sleep(0.02)
    while pressed(btn_cal) is False:
        time.sleep(0.02)
    time.sleep(0.25)
    V_white = sensor.read_u16()

    # Ensure ordering
    lo = min(V_black, V_white)
    hi = max(V_black, V_white)
    V_black, V_white = lo, hi

    V_mid = (V_black + V_white) / 2.0

    mqtt_pub(config.TOPIC_EVENTS, {
        "ts": now_iso(),
        "run_id": run_id,
        "robot_id": config.ROBOT_ID,
        "event": "calibrated",
        "payload": {
            "black_u16": V_black,
            "white_u16": V_white,
            "mid_u16": V_mid
        }
    })

# ---------- Line validity ----------
def is_valid_reading(u16):
    if V_black is None or V_white is None:
        return True  # if not calibrated, assume valid
    margin = int((V_white - V_black) * config.VALID_MARGIN)
    return (V_black - margin) <= u16 <= (V_white + margin)

def bias_from_steer(steer: float):
    # If we were turning left before lost, search left first
    return "LEFT" if steer < 0 else "RIGHT"

# ---------- Main control ----------
def control_step():
    global seq, last_err, last_t, lost_since

    u16 = sensor.read_u16()
    ts = now_iso()

    # Lost-line detection
    valid = is_valid_reading(u16)
    if not valid:
        if lost_since is None:
            lost_since = time.ticks_ms()
        lost_ms = time.ticks_diff(time.ticks_ms(), lost_since)
    else:
        lost_since = None
        lost_ms = 0

    # If in recovery, keep trying until valid
    if recovery.active:
        # If recovered:
        if valid:
            recovery.stop()
            mqtt_pub(config.TOPIC_EVENTS, {
                "ts": ts, "run_id": run_id, "robot_id": config.ROBOT_ID,
                "event": "recovered", "payload": {}
            })
        else:
            recovery.step(motorL, motorR)
            # Telemetry still can be published
            return u16, 0.0, 0.0, True, lost_ms

    # Start recovery if lost too long
    if lost_since is not None and lost_ms > config.LOST_MS:
        # Decide bias using last control output sign (approx via last_err)
        steer_hint = -(last_err)  # rough: if err says line is left/right
        bias = bias_from_steer(steer_hint)

        recovery.start(bias=bias)
        mqtt_pub(config.TOPIC_EVENTS, {
            "ts": ts, "run_id": run_id, "robot_id": config.ROBOT_ID,
            "event": "lost_line",
            "payload": {
                "lost_ms": lost_ms,
                "bias": bias,
                "sensor_u16": u16
            }
        })
        # In RECOVERY, do one step immediately
        recovery.step(motorL, motorR)
        return u16, 0.0, 0.0, True, lost_ms

    # Normal PD control
    if V_mid is None:
        # if not calibrated, stop safely
        motorL.set(0.0)
        motorR.set(0.0)
        return u16, 0.0, 0.0, False, 0

    # Error: choose sign convention
    # If u16 increases toward white and decreases toward black, error relative to mid:
    err = (V_mid - u16) / (V_white - V_black + 1e-9)  # normalize approx to -1..+1
    err = clamp(err, -1.0, 1.0)

    t = time.ticks_ms()
    dt = time.ticks_diff(t, last_t) / 1000.0
    dt = max(dt, 1e-3)
    derr = (err - last_err) / dt

    steer = config.Kp * err + config.Kd * derr
    steer = clamp(steer, -0.8, 0.8)

    base = config.BASE_SPEED
    left = clamp(base - steer, -1.0, 1.0)
    right = clamp(base + steer, -1.0, 1.0)

    # enforce min/max forward speed
    left = clamp(left, config.MIN_SPEED, config.MAX_SPEED)
    right = clamp(right, config.MIN_SPEED, config.MAX_SPEED)

    motorL.set(left)
    motorR.set(right)

    last_err = err
    last_t = t

    # Segment memory update (emit segment change as event)
    seg = segmenter.update(steer=steer, lost=False)
    if seg:
        mqtt_pub(config.TOPIC_EVENTS, {
            "ts": ts, "run_id": run_id, "robot_id": config.ROBOT_ID,
            "event": "segment",
            "payload": seg
        })

    return u16, err, steer, False, 0

def main():
    global run_id, seq

    print("[BOOT] Starting...")
    try:
        mqtt_init()
        mqtt_pub(config.TOPIC_EVENTS, {
            "ts": now_iso(), "run_id": None, "robot_id": config.ROBOT_ID,
            "event": "robot_online", "payload": {}
        })
    except Exception as e:
        print("[NET] MQTT not available:", e)

    print("[INFO] Press CAL (GP21) to calibrate. Press START (GP20) to run.")
    run_id = gen_run_id()

    # Wait calibration
    while V_mid is None:
        if pressed(btn_cal):
            time.sleep(0.25)
            do_calibration()
        time.sleep(0.02)

    # Wait start
    while not pressed(btn_start):
        # process incoming commands if MQTT is up
        try:
            if mqtt: mqtt.check_msg()
        except Exception:
            pass
        time.sleep(0.02)

    time.sleep(0.25)  # debounce
    run_id = gen_run_id()
    mqtt_pub(config.TOPIC_EVENTS, {
        "ts": now_iso(),
        "run_id": run_id,
        "robot_id": config.ROBOT_ID,
        "event": "run_start",
        "payload": {
            "controller": "PD",
            "kp": config.Kp,
            "kd": config.Kd,
            "base_speed": config.BASE_SPEED
        }
    })

    # Scheduling
    control_period_ms = int(1000 / config.CONTROL_HZ)
    telemetry_period_ms = int(1000 / config.TELEMETRY_HZ)
    t_control = time.ticks_ms()
    t_tele = time.ticks_ms()

    while True:
        now = time.ticks_ms()

        # Control tick
        if time.ticks_diff(now, t_control) >= control_period_ms:
            t_control = now
            u16, err, steer, lost, lost_ms = control_step()
            seq += 1

        # Telemetry tick (lower rate)
        if time.ticks_diff(now, t_tele) >= telemetry_period_ms:
            t_tele = now
            try:
                line_v = read_voltage_u16(u16)
            except Exception:
                line_v = None

            mqtt_pub(config.TOPIC_TELEMETRY, {
                "ts": now_iso(),
                "run_id": run_id,
                "robot_id": config.ROBOT_ID,
                "seq": seq,
                "sensor": {
                    "line_u16": u16,
                    "line_v": line_v,
                    "err": err
                },
                "pid": {  # keep field name "pid" for compatibility, even if PD
                    "kp": config.Kp,
                    "kd": config.Kd,
                    "out": steer
                },
                "motors": {
                    "base": config.BASE_SPEED,
                    "left": None,   # optional: store last command if you track it
                    "right": None
                }
            })

        # MQTT receive (best effort)
        try:
            if mqtt:
                mqtt.check_msg()
        except Exception:
            pass

        # Optional: stop on START button press again
        if pressed(btn_start):
            time.sleep(0.25)
            motorL.set(0.0)
            motorR.set(0.0)
            mqtt_pub(config.TOPIC_EVENTS, {
                "ts": now_iso(), "run_id": run_id, "robot_id": config.ROBOT_ID,
                "event": "run_stop", "payload": {}
            })
            break

        # tiny sleep to yield CPU
        time.sleep_ms(1)

if __name__ == "__main__":
    main()