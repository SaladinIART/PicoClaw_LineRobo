# Backend Services (Docker)

The laptop runs several containerized services that support the robot.

These services are orchestrated using Docker Compose.

---

## Service Components

### Mosquitto MQTT Broker

Handles communication between the robot and backend services.

Responsibilities:

- receive telemetry messages
- distribute messages to subscribers

MQTT is lightweight and commonly used in IoT systems.

---

### Logger Service

A Python service that listens to telemetry messages and stores them in a database.

Responsibilities:

- subscribe to MQTT topics
- store data in SQLite
- record robot events
- allow later analysis

---

### SQLite Database

SQLite is used for simplicity.

Advantages:

- no external database server required
- easy to export data
- lightweight

Stored data includes:

- telemetry logs
- robot events
- run identifiers

---

### SQLite Web Viewer

A small web interface allows viewing the database in a browser.

Example tables:

- runs
- telemetry
- events

---

## Why Containers?

Using Docker allows:

- easy deployment
- consistent environment
- portable system setup

The entire backend can be started with:

docker compose up