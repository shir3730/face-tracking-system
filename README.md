# Real-Time Face Tracking System (Host-Target Architecture) 🎥

This project implements a closed-loop face tracking system using a **Host-Target architecture**. 
The system delegates heavy visual processing to a PC (Host) while maintaining precise hardware control on a Microcontroller (Target).

## 🧠 System Architecture

1. **Host PC (Python + OpenCV):** - Captures video feed and detects faces using the Haar Cascade algorithm.
   - Optimizes performance by processing frames in Grayscale.
   - Calculates the spatial deviation (offset) from the center.
   - Transmits error data via UART communication.

2. **Target MCU (C/C++ - Arduino):**
   - Receives offset data and executes a stabilized control loop.
   - **Deadband Logic:** Implements a ±50-pixel deadband to ignore optical noise and minor user movements (breathing/swaying).
   - **Incremental Tracking:** Addresses latency by moving the servo in precise ∓1-degree increments.
   - **Software Clamping:** Protects hardware by limiting servo movement to 0°-180°.

## 🛠️ Hardware Requirements
* Arduino (or any compatible MCU)
* Servo Motor (connected to pin 9)
* USB Webcam
