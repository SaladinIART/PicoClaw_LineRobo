# PicoClaw Line Following Robot
### AI-Assisted Robotics Architecture (Design + Prototype)

---

## Introduction

Imagine a small robot that follows a black line on the floor, notices when it makes a mistake, and sends updates to your computer so its performance can be analyzed and improved.

**PicoClaw LineRobo** explores how a simple robot can be designed using the same architecture principles used in industrial automation and robotics systems.

Instead of focusing only on making a robot move, this project focuses on building a **complete system around the robot**, including:

- real-time control
- data logging
- system monitoring
- future AI-assisted improvements

Even though the robot hardware is simple, the system design reflects how modern robotic platforms are structured.

If you are new to robotics or some terms are unfamiliar, see the **Glossary** section at the end of this document.

---

# What This Project Does

The robot performs several basic tasks:

- Detect a black line on the ground
- Follow the line using sensor feedback
- Detect when it loses the line
- Attempt recovery automatically
- Send performance data to a computer

While the robot moves, it continuously reports what it is doing.

Examples of information sent to the computer include:

- sensor readings
- steering corrections
- motor speed
- error events (such as losing the line)

This information can later be used to understand how the robot behaves and how it can improve.

---

# Why This Project Matters

Many simple robots use very basic logic like:

> “If the sensor sees black, move forward.”

This project explores a more advanced approach by separating the system into three layers:

1️⃣ **Robot Control Layer**  
Handles real-time movement and sensor processing.

2️⃣ **Data Logging Layer**  
Collects and stores robot performance data.

3️⃣ **AI Advisory Layer (planned)**  
Analyzes past data and suggests improvements.

This layered design prevents delays or network problems from affecting the robot’s movement.

The robot always remains autonomous.

---

# System Overview

The system is divided into two main parts: the robot and the computer.

Robot (Pico W Microcontroller)
│
├ Line Sensor
├ Motor Driver
├ Steering Controller
├ Error Detection
└ WiFi Telemetry
│
│ WiFi
▼
Computer (Docker Services)
│
├ MQTT Communication Server
├ Data Logger
└ SQLite Database
│
▼
Future AI Analysis (PicoClaw)


The robot performs the real-time work while the computer collects and analyzes information.

---

# What the Robot Actually Does

The robot contains three main components:

### Sensors
A line sensor detects the difference between the black track and the white floor.

### Controller
A steering algorithm adjusts the robot’s motors so it stays centered on the line.

Think of this like how a driver constantly adjusts the steering wheel to stay in the lane.

### Recovery System

If the robot loses the line, it does not panic.

Instead, it follows a simple recovery plan:

1. Stop briefly  
2. Reverse slightly  
3. Rotate to search for the line  
4. Resume normal movement once the line is found

This prevents the robot from wandering randomly.

---

# Why the Robot Sends Data to a Computer

While the robot runs, it sends updates through WiFi.

This communication uses a lightweight messaging method commonly used in Internet-of-Things systems.

The computer stores the robot’s activity in a small database.

This allows us to later analyze:

- how smoothly the robot drove
- where it struggled
- how often it lost the track
- how the steering system behaved

This is similar to how factories monitor machines to improve performance.

---

# The "Imaginary Map" Idea

The robot does not use GPS or cameras.

Instead, it creates a **simple memory of the track** based on its behavior.

For example, it may detect patterns like:

- straight section
- gentle left turn
- sharp right turn

This type of representation is called **topological mapping**.

The robot does not know exact coordinates, but it remembers patterns in the track.

This helps guide recovery behavior when the robot loses the line.

---

# Planned AI Integration (PicoClaw)

This project proposes integrating a future AI system called **PicoClaw**.

The AI would analyze recorded telemetry and suggest improvements.

Examples include:

- detecting unstable steering behavior
- recommending better control settings
- suggesting improved recovery strategies
- identifying problematic track sections

Importantly, the AI **does not control the robot directly**.

Instead, it works as an advisor.

This keeps the robot stable and predictable.

---

# Technologies Used

## Robot Side

- MicroPython firmware
- Sensor-based steering control
- Error detection and recovery logic
- WiFi telemetry communication

## Computer Side

- Docker container environment
- MQTT messaging server
- Python logging service
- SQLite database

---

# Current Limitations

This project intentionally uses minimal hardware.

The robot currently does not include:

- wheel encoders
- motion sensors
- cameras or LIDAR

Because of this, the robot cannot determine its exact position or distance traveled.

Instead, it uses simple sensor feedback to stay on the track.

---

# Future Improvements

Possible future upgrades include:

- wheel encoders for distance measurement
- motion sensors for orientation tracking
- multi-sensor line detection
- visual dashboards for telemetry data
- AI-assisted controller tuning

These upgrades would allow the robot to perform more advanced navigation tasks.

---

# Repository Structure

firmware/micropython
Robot firmware code

services/logger
Data logging service

services/mosquitto
MQTT communication configuration

docker-compose.yml
Container orchestration

docs/
Architecture documentation

data/
Local database storage

---

# Engineering Focus

This project demonstrates several important engineering concepts:

- embedded system design
- feedback control systems
- fault detection and recovery
- distributed system architecture
- telemetry data pipelines
- containerized backend services

Even with limited hardware resources, the project shows how robotic systems can be designed in a scalable and modular way.

---

# Final Thoughts

Although the robot itself is simple, the architecture behind it reflects the design philosophy used in modern robotics and automation systems.

The goal of this project is to explore **how small robotics platforms can evolve into intelligent, data-driven systems.**
