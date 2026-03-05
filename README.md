📌 PicoClaw Line Following Robot
AI-Assisted Robotics Architecture (Design + Prototype)
🌍 What Is This Project?

This project explores how a small robot can:

-Follow a black line on the floor

-Detect when it gets lost

-Recover intelligently

-Send performance data to a computer

-Use AI to analyze its behavior

Even though the robot hardware is simple, the system is designed like a modern industrial robotic system.

The focus of this project is not just “making a robot move,”
but designing a complete robotics architecture.

🧠 Why This Project Matters

Most small robots are programmed with simple logic:

“If sensor sees black, go forward.”

This project goes further.

It separates the system into:

🟢 Real-time control (robot)

🟠 Data collection (computer)

🔵 AI analysis (advisory system)

This is similar to how industrial automation systems are built.

🏗 System Overview (Simple Explanation)

Robot (Pico W)
   ↓ sends data over WiFi
Computer (Docker services)
   ↓ stores data in database
AI system analyzes performance

The robot runs independently.
The computer does not directly control the motors.

This prevents delays or instability.

🤖 What the Robot Does

The robot contains:

-A line sensor (to detect black vs white surface)

-Motors

-A microcontroller (Raspberry Pi Pico W)

The robot can:

1. Calibrate the sensor

2. Follow the line using a control algorithm

3. Detect when it loses the line

4. Attempt recovery automatically

5. Send performance data to a laptop

The robot keeps working even if WiFi disconnects.

📡 Why WiFi and Data Logging?

While the robot runs, it sends:

- Sensor values

- Steering corrections

- Motor speed

- Events (lost line, recovery, segment changes)

The computer stores this in a database.

This allows:

- Performance analysis

- Debugging

- Future AI improvements

- Comparing lap times

This is how industrial systems monitor machines in factories.

🗺 “Imaginary Map” Concept

The robot does not use GPS or cameras.

Instead, it builds a logical memory of the track:

- Straight sections

- Left curves

- Right curves

- Sharp turns

This is called topological mapping.

It doesn’t know exact coordinates,
but it remembers behavior patterns.

This allows smarter recovery decisions.

🧠 Planned AI Integration (PicoClaw)

The AI system is designed to:

- Analyze past telemetry

- Detect oscillation or instability

- Suggest better tuning values

- Suggest improved recovery strategies

Important:

The AI does NOT directly control the motors in real time.

It only advises when:

- The robot gets lost

- A run ends

- Performance needs tuning

This keeps the system stable and safe.

🛠 Technologies Used
Robot Side

- MicroPython

- PD Control Algorithm

- State Machine Recovery

- MQTT Communication

Computer Side

- Docker Containers

- Mosquitto MQTT Broker

- Python Logger Service

- SQLite Database

🎯 Engineering Focus

This project demonstrates:

- Embedded systems thinking

- Control systems design

- Fault detection and recovery logic

- Distributed architecture

- Containerized backend services

- Data logging pipeline

- AI integration planning

- Robotics systems engineering

🚧 Current Limitations

- No wheel encoders (no distance measurement)

- No IMU (no orientation tracking)

- No spatial mapping (no SLAM)

- Single loop track (no path branching)

These limitations are hardware-based, not architectural.

🚀 Future Improvements

Possible upgrades:

- Add wheel encoders

- Add IMU

- Add junction detection

- Add path planning algorithm

- Add dashboard visualization (Grafana)

- Complete PicoClaw advisory container

📁 Repository Structure

firmware/micropython     → Robot control code
services/logger          → Data logging container
services/mosquitto       → MQTT configuration
docker-compose.yml       → System orchestration
data/                    → SQLite database
docs/                    → Architecture notes

🧭 What This Project Really Shows

Even with limited hardware, this project shows:

- How to design systems like industrial robotics

- How to separate real-time control from AI processing

- How to build scalable architecture

- How to think like a systems engineer

This is not just a toy robot.

It is a prototype of an AI-assisted robotic system architecture.

🔚 Final Thought

This project represents:

A structured robotics systems architecture design with embedded control, distributed telemetry, and AI advisory integration.

It reflects systems thinking, not just coding.