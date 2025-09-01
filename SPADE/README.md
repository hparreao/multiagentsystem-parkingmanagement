# SPADE Parking Management System

## Overview

This directory contains the multi-agent system implementation for the parking management system using the SPADE framework.

## Directory Structure

```
SPADE/
├── parking_system/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── Driver.py
│   │   ├── ParkingManager.py
│   │   ├── ParkingSpotModule.py
│   │   └── ParkingZoneManager.py
│   ├── api/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── constants.py
│   └── example.py
├── main.py
├── requirements.txt
└── README.md
```

## Components

### Agents

1. **Driver Agent**: Represents a driver looking for a parking spot
2. **ParkingManager Agent**: Manages the entire parking system
3. **ParkingZoneManager Agent**: Manages a specific parking zone
4. **ParkingSpotModule Agent**: Represents an individual parking spot with sensor

### API

The system exposes a REST API through FastAPI for interaction with external systems and the mobile application.

### Constants

Shared constants used across the system are defined in `constants.py`.

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the system:
   ```bash
   python main.py
   ```

The server will start on `http://localhost:8000`.

## Usage

See `example.py` for a complete example of how to use the system.