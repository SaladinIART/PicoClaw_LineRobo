import time
import network
from umqtt.simple import MQTTClient

def wifi_connect(ssid: str, password: str, timeout_s: int = 15):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if wlan.isconnected():
        return wlan
    wlan.connect(ssid, password)
    t0 = time.time()
    while not wlan.isconnected():
        if time.time() - t0 > timeout_s:
            raise RuntimeError("Wi-Fi connect timeout")
        time.sleep(0.2)
    return wlan

def mqtt_connect(client_id: str, host: str, port: int):
    c = MQTTClient(client_id=client_id, server=host, port=port, keepalive=30)
    c.connect()
    return c