# AI Advisory System (PicoClaw Concept)

This project proposes integrating an AI system called **PicoClaw**.

PicoClaw acts as an **advisor**, not a direct controller.

---

## Why Not Control Motors with AI?

AI systems may introduce:

- network latency
- unpredictable delays
- unstable control loops

For safety, **real-time control remains on the microcontroller**.

---

## PicoClaw Responsibilities

The AI system would analyze telemetry data and suggest improvements.

Possible functions:

- detect oscillation patterns
- recommend PID parameter adjustments
- suggest recovery strategies
- identify problematic track segments

---

## Example Workflow

Robot detects lost line.

Robot sends event:

lost_line

Backend retrieves recent telemetry.

PicoClaw analyzes:

- steering behaviour
- sensor values
- previous segment patterns

AI suggests:

reduce speed or adjust controller parameters.

---

## Benefits

This hybrid architecture combines:

- deterministic control
- data-driven improvement
- AI assisted diagnostics

It mirrors how modern **industrial robotics systems** integrate analytics.