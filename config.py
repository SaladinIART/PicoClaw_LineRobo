# Wi-Fi
WIFI_SSID = Muhd Yusuf_5G@allo
WIFI_PASS = muhdyusuf@2233

# MQTT broker (your laptop LAN IP)
MQTT_HOST = "192.168.0.6"   # <-- change to your laptop IP on same Wi-Fi
MQTT_PORT = 1883

# MQTT topics
TOPIC_TELEMETRY = b"bocobot/telemetry"
TOPIC_EVENTS    = b"bocobot/events"
TOPIC_CMD       = b"bocobot/cmd"

ROBOT_ID = "bocobot-01"

# Control loop
CONTROL_HZ = 80              # 50–100 is fine
TELEMETRY_HZ = 20            # keep lower than control loop

# Line sensor ADC
LINE_ADC_PIN = 26            # GP26 (ADC0) common choice on ROBO-PICO Grove ADC :contentReference[oaicite:3]{index=3}

# Motor pins (ROBO-PICO motor terminals)
# M1A=GP8, M1B=GP9, M2A=GP10, M2B=GP11 :contentReference[oaicite:4]{index=4}
M1A = 8
M1B = 9
M2A = 10
M2B = 11

# Buttons (ROBO-PICO programmable buttons)
# GP20 and GP21 :contentReference[oaicite:5]{index=5}
BTN_START = 20
BTN_CAL   = 21

# PD gains (start conservative; tune later)
Kp = 0.9
Kd = 0.08

# Speed limits (throttle is -1.0..+1.0)
BASE_SPEED = 0.50
MAX_SPEED  = 0.75
MIN_SPEED  = 0.10

# Lost-line detection
LOST_MS = 450                # if lost for > this duration -> RECOVERY
VALID_MARGIN = 0.08          # widen/narrow based on your sensor stability

# Recovery behavior
RECOVERY_TIMEOUT_MS = 2500
RECOVERY_SPIN_SPEED = 0.25
RECOVERY_REVERSE_SPEED = -0.25
RECOVERY_REVERSE_MS = 220
RECOVERY_SPIN_MS = 500