# Project Limitations

This project intentionally uses minimal hardware.

The goal is to explore **architecture and system design** rather than complex sensing.

---

## Hardware Limitations

The robot currently lacks:

- wheel encoders
- inertial measurement unit (IMU)
- camera or LIDAR

Because of this, the robot cannot perform:

- spatial mapping
- SLAM
- accurate position tracking

---

## Navigation Limitations

The robot follows a **single line track**.

There are no:

- intersections
- path branches
- alternative routes

Therefore algorithms like A* path planning are not applicable.

---

## Mapping Approach

Instead of spatial mapping, the robot uses **topological mapping**.

This means it identifies patterns such as:

- straight sections
- left turns
- right turns

This behavioural representation is sufficient for line-following tasks.

---

## Resource Constraints

The project was conducted with limited hardware resources.

As a result, some planned features remain conceptual.

However, the system architecture supports future expansion.