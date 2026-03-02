📌 PicoClaw Line Following Robot (AI-Integrated Architecture)
Overview

This project designs and prototypes an AI-assisted line following robot using:

-Raspberry Pi Pico W (MicroPython)

-MQTT communication

-Docker-based backend services

-SQLite data logging

-Planned PicoClaw AI advisory integration

The objective is to demonstrate:

-Real-time embedded control

-Distributed system architecture

-Telemetry logging pipeline

-AI-assisted recovery and tuning strategy

🧠 System Architecture

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

🔧 Firmware Capabilities

-Calibration via button (black/white capture)

-PD line following controller

-Lost-line detection with recovery behavior

-Segment classification (topological track memory)

-MQTT telemetry publishing

-Event publishing (run_start, lost_line, segment, etc.)

📊 Data Logging System

-Backend services include:

-MQTT Broker (Mosquitto)

-Python Logger container

-SQLite database

-SQLite Web viewer

-Telemetry stored:

-Timestamp

-Sensor voltage

-Error value

-PID output

-Motor command

-Segment classification

-Events

🤖 Planned PicoClaw Integration

The AI component is designed to:

-Analyze recent telemetry

-Suggest recovery strategies

-Suggest parameter tuning (Kp, Kd, base speed)

-Detect oscillation patterns

-Identify problematic track segments

Architecture supports AI advisory without affecting real-time control loop.

🚧 Limitations

-No wheel encoders (no metric mapping)

-No IMU or SLAM capability

-Topological mapping only (segment-based)

-A* pathfinding not applicable due to single-loop track

🛣 Future Improvements

-Add wheel encoders for distance estimation

-Add IMU for orientation tracking

-Add junction detection for graph-based navigation

-Implement PicoClaw recovery advisor container

-Add Grafana dashboard

📁 Repository Structure

firmware/micropython     → Pico W embedded firmware
services/logger          → Telemetry logging container
services/mosquitto       → MQTT broker config
docker-compose.yml       → System orchestration
data/                    → SQLite database
docs/                    → Architecture documentation

🧩 Engineering Focus

This project demonstrates:

-Embedded systems design

-Control systems (PD controller)

-Distributed architecture

-Containerization (Docker)

-Telemetry and logging pipelines

-AI integration planning

-Robotics systems engineering thinking