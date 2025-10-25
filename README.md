# AI Car MVP

An intelligent car assistant system that responds to voice commands and controls various car functions.

## Project Structure

```
ai-car/
├── app/                    # Main application code
│   ├── main.py            # Application entry point
│   ├── audio_io.py        # Audio input/output handling
│   ├── boson_api.py       # Boson AI API integration
│   ├── dispatcher.py      # Command routing
│   ├── device/            # Hardware interfaces
│   │   └── car.py         # Car hardware control
│   ├── intents/           # Natural language understanding
│   │   ├── __init__.py
│   │   ├── types.py       # Intent data structures
│   │   ├── rules.py       # Intent processing logic
│   │   ├── rules.yaml     # Intent configuration
│   │   └── registry.py    # Intent handler registry
│   └── commands/          # Executable commands
│       ├── __init__.py
│       ├── navigate.py    # Navigation commands
│       ├── play_radio.py  # Radio/audio commands
│       └── estop.py       # Emergency stop commands
├── demo/                  # Demo and testing
│   ├── routes.py         # Sample routes
│   └── stations.json     # Radio stations
├── firmware/              # ESP32 firmware
│   └── esp32_car/        # Car controller firmware
│       ├── platformio.ini
│       └── src/main.cpp
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── Makefile              # Build commands
└── README.md             # This file
```

## Getting Started

1. Copy `.env.example` to `.env` and configure your settings
2. Install dependencies: `make install`
3. Build firmware: `make firmware`
4. Run demo: `make demo`

## Features

- Voice command recognition
- Natural language processing
- Car hardware control
- Radio/audio management
- Navigation assistance
- Emergency stop functionality

## Hardware Requirements

- ESP32 development board
- Microphone and speaker
- Car interface hardware
- USB connection for programming

## Development

This is an MVP (Minimum Viable Product) for an AI-powered car assistant system.
