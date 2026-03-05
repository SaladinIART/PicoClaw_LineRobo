---

# Glossary

This section explains some technical terms used in this project in simple language.

### Microcontroller
A very small computer designed to control hardware such as sensors, motors, and lights.  
In this project, the robot uses a **Raspberry Pi Pico W** as its microcontroller.

---

### MicroPython
A lightweight version of the Python programming language designed for small devices like microcontrollers.

It allows developers to write simple Python code that runs directly on embedded hardware.

---

### Control Algorithm
A method used to adjust the robot’s movement based on sensor input.

In this project, the robot constantly adjusts its motor speed so it stays on the line.

You can think of it like a driver slightly turning the steering wheel to stay in a lane.

---

### PD Controller
Short for **Proportional–Derivative Controller**.

It is a simple control method that helps the robot steer smoothly by correcting errors in its position relative to the line.

Instead of reacting only to where the robot is, it also considers how quickly the robot is drifting away from the line.

---

### Telemetry
Telemetry means **collecting and sending data from a device to another system for monitoring**.

The robot sends telemetry such as:

- sensor readings  
- steering corrections  
- motor speed  
- error events

This data helps analyze the robot’s performance.

---

### MQTT
MQTT is a lightweight communication protocol often used in Internet-of-Things (IoT) systems.

It allows devices to send messages to each other over a network in a simple and efficient way.

In this project, MQTT is used for the robot to send telemetry data to the computer.

---

### Docker
Docker is a tool used to run software inside isolated environments called **containers**.

Containers make it easier to run services like databases and servers without complicated installation.

In this project, Docker runs the backend services such as:

- MQTT broker
- data logger
- database tools

---

### SQLite
SQLite is a lightweight database used to store data locally in a single file.

It does not require a separate database server and is commonly used in embedded systems and small applications.

In this project, SQLite stores robot telemetry and event logs.

---

### Topological Mapping
A simplified way of representing an environment using **patterns and relationships instead of exact coordinates**.

For example, the robot might recognize:

- straight section
- left turn
- right turn

instead of knowing the exact physical position.

---

### State Machine
A structured way of designing robot behavior using different states.

For example, the robot may operate in states such as:

- calibration
- waiting to start
- following the line
- recovery mode

Each state defines what the robot should do.

---

### Telemetry Logger
A backend program that collects and stores telemetry data from the robot.

In this project, a Python logging service stores robot data inside an SQLite database.

---

### AI Advisory System
A planned feature where an AI system analyzes past telemetry data and suggests improvements to the robot’s behavior.

The AI does not directly control the robot but provides recommendations.

This approach helps maintain stable real-time control.

---