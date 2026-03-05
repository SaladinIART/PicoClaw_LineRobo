# System Architecture Diagram

This project uses a **distributed robotics architecture**.

The robot performs real-time control locally, while a computer handles
data collection and future AI analysis.

This separation prevents network delays from affecting robot movement.

---

## System Overview

Robot (Raspberry Pi Pico W)
│
├─ Line Sensor (ADC)
├─ Motor Driver
├─ PD Controller
├─ Lost Line Detection
└─ MQTT Telemetry
│
│ WiFi Communication
▼
Laptop (Docker Environment)
│
├─ Mosquitto MQTT Broker
│
├─ Logger Service
│ └─ Stores telemetry in SQLite
│
└─ Future: PicoClaw AI Advisor
└─ Analyze robot behaviour
---

## Data Flow

Robot → MQTT → Logger → SQLite Database → Analysis

The robot publishes data such as:

- sensor readings  
- steering corrections  
- motor commands  
- system events  

These are stored for later analysis and tuning.

---

## Design Philosophy

The robot must always remain **autonomous and stable**.

Therefore:

- Control loop runs on microcontroller
- AI only provides suggestions
- Network latency cannot affect motor control

This design follows common principles used in **industrial automation systems**.