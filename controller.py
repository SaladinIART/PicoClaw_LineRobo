import time
from machine import Pin, PWM, ADC

def clamp(x, lo, hi):
    return lo if x < lo else (hi if x > hi else x)

class MotorHBridge:
    """
    Simple 2-pin per motor control:
    - forward: PWM on A, B off
    - backward: PWM on B, A off
    Pin mapping matches ROBO-PICO motor inputs: GP8/9, GP10/11 :contentReference[oaicite:6]{index=6}
    """
    def __init__(self, pin_a: int, pin_b: int, pwm_hz: int = 20000):
        self.pwm_a = PWM(Pin(pin_a))
        self.pwm_b = PWM(Pin(pin_b))
        self.pwm_a.freq(pwm_hz)
        self.pwm_b.freq(pwm_hz)
        self.set(0.0)

    def set(self, throttle: float):
        # throttle: -1..+1
        t = clamp(throttle, -1.0, 1.0)
        if t >= 0:
            duty = int(t * 65535)
            self.pwm_a.duty_u16(duty)
            self.pwm_b.duty_u16(0)
        else:
            duty = int((-t) * 65535)
            self.pwm_a.duty_u16(0)
            self.pwm_b.duty_u16(duty)

class LineSensor:
    def __init__(self, adc_pin: int):
        self.adc = ADC(Pin(adc_pin))
    def read_u16(self) -> int:
        return self.adc.read_u16()