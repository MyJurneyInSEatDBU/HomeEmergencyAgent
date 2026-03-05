# Introduction to Smart Bulb Control System (Simple Reflex Agent)

## 1. Project Overview

The Smart Bulb Control System is a graphical simulation of an automatic lighting system designed using Python Tkinter. It demonstrates the concept of a Simple Reflex Agent, where the system reacts to environmental changes (simulated motion) and controls the state of a bulb (ON/OFF) accordingly. This project provides a visual, interactive interface that mimics a smart lighting system, commonly used in smart homes, offices, and automated buildings.

## 2. Objective

The main objectives of the project are:

- **Demonstrate a Simple Reflex Agent:** The system reacts directly to the input (motion detection) without memory of past states.
- **Simulate an automatic bulb system in Python:** Provides an interactive GUI for testing the concept without physical hardware.
- **Visual representation of bulb state:** Shows the bulb ON/OFF with visual effects and status indicators.
- **Introduce motion-based automation concepts:** Lays the groundwork for real-world implementation using sensors like PIR or LDR.

## 3. System Components

The system consists of:

### Graphical User Interface (GUI)

Developed using Tkinter.  
Modern, interactive layout with gradient backgrounds, 3D-like bulb visualization, and styled buttons.

### Bulb State Simulation

- **ON state:** Glowing yellow with animation.  
- **OFF state:** Dark gray, no glow.

### Motion Detection Simulation

Controlled by buttons:

- **“Person Enters”** → simulate motion detected → bulb turns ON.  
- **“Person Leaves”** → simulate no motion → bulb turns OFF.

Motion indicator shows current motion status.

### Notifications

Popup-like messages provide feedback whenever a person enters, leaves, or the system resets.