# Robot Firmware Architecture

The robot firmware runs on a **Raspberry Pi Pico W** using MicroPython.

Its responsibility is to perform all **real-time operations**, including:

- reading sensors
- controlling motors
- detecting errors
- publishing telemetry

---

## Firmware Components

### main.py

Entry point for the robot.

Responsibilities:

- initialize hardware
- start control loop
- handle calibration
- publish telemetry
- manage robot states

---

### controller.py

Implements the line following algorithm.

Main functions:

- calculate steering corrections
- apply PD control logic
- generate motor commands

---

### net_mqtt.py

Handles network communication.

Responsibilities:

- connect to WiFi
- connect to MQTT broker
- publish telemetry messages
- receive commands

---

### config.py

Central configuration file.

Contains:

- WiFi credentials
- MQTT topics
- controller parameters
- motor limits
- recovery behaviour settings

---

## Robot State Machine

The robot operates using a simple state machine.

CALIBRATION
↓
WAIT_START
↓
FOLLOW_LINE
↓
LOST_LINE
↓
RECOVERY
↓
FOLLOW_LINE

---

## Recovery Behaviour

When the robot loses the line:

1. Stop briefly
2. Reverse slightly
3. Rotate to search for the line
4. Resume normal control when the line is detected

This prevents the robot from wandering randomly.

---

## Telemetry Data

The robot publishes telemetry periodically:

- sensor voltage
- steering error
- motor speeds
- controller output

Events are also reported:

- run_start
- lost_line
- recovered
- segment_change