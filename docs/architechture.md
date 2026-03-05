Pico W (MicroPython Firmware)
│
├── Sensor Read (ADC)
├── PD Controller
├── Lost-Line Detection
├── Recovery State Machine
└── MQTT Telemetry
        ↓ WiFi
----------------------------
Laptop (Docker Stack)
│
├── Mosquitto (MQTT Broker)
├── Logger Service (SQLite)
└── Future: PicoClaw Bridge
        └── AI Advisory System

Notes:
Control Philosophy

Real-time control remains on microcontroller.

AI advisory operates asynchronously.

Recovery decisions are:

event-triggered

not continuous motor commands

latency tolerant

This avoids real-time instability.