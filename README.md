# AI Car Voice Assistant - MVP

A laptop-hosted voice assistant that controls an RC car via voice commands. The system uses push-to-talk (PTT) interaction, transcribes speech using Boson AI's ASR, processes intents, and controls the car through a simple device API.

**Current Status:** Phase 2 Complete - ASR Integration ✓

## Project Overview

This MVP demonstrates a voice-controlled car assistant with these capabilities:
- Push-to-talk voice input
- Automatic speech recognition (ASR) via Boson AI
- Intent-based command routing
- Simulated car control (hardware integration in later phases)
- Text-to-speech (TTS) responses

## Quick Start

### Prerequisites

- Python 3.8+ 
- A working microphone
- Boson AI API key ([Get it here](https://hackathon.boson.ai))

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd ai-car
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   make install
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your BOSON_API_KEY
   ```

### Running the Application

Start the voice assistant:
```bash
make run
```

**Usage:**
1. Press `Enter` to activate push-to-talk
2. Speak your command (recording lasts 2.5 seconds)
3. View the transcription in the console
4. Press `Enter` again for another command
5. Press `Ctrl+C` to exit

## Project Structure

```
ai-car/
├── app/                      # Main application code
│   ├── __init__.py          # Package initialization
│   ├── main.py              # Application entry point with PTT loop
│   ├── logging_cfg.py       # Centralized logging configuration
│   ├── audio_io.py          # Microphone recording (PTT)
│   ├── boson_api.py         # Boson AI API integration (ASR/TTS)
│   ├── dispatcher.py        # Command routing (Phase 4)
│   ├── device/              # Hardware interfaces
│   │   ├── car_base.py      # Abstract car interface
│   │   ├── car_sim.py       # Simulated car (Phase 6)
│   │   └── car_serial.py    # Serial car interface (Phase 7+)
│   ├── intents/             # Natural language understanding
│   │   ├── __init__.py
│   │   ├── types.py         # Intent data structures
│   │   ├── rules.py         # Rule-based intent matching
│   │   ├── rules.yaml       # Intent patterns
│   │   ├── registry.py      # Intent-to-handler mapping
│   │   └── fallback_llm.py  # LLM-based intent fallback
│   └── commands/            # Command handlers
│       ├── __init__.py
│       ├── navigate.py      # Navigation commands
│       ├── play_radio.py    # Radio/audio commands
│       └── estop.py         # Emergency stop
├── demo/                    # Demo data
│   ├── routes.py           # Pre-scripted routes
│   └── stations.json       # Radio station definitions
├── tests/                   # Unit tests
│   ├── test_rules.py       # Intent rule tests
│   └── test_dispatch.py    # Dispatcher tests
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── Makefile                # Build/run commands
└── README.md               # This file
```

## Configuration

Edit `.env` to configure the application:

```bash
# Boson AI API
BOSON_API_KEY=your_api_key_here
BOSON_BASE_URL=https://hackathon.boson.ai/v1

# Audio Settings
AUDIO_SAMPLE_RATE=24000      # 24kHz recommended for Boson
PTT_SECONDS=2.5              # Recording duration
TTS_VOICE=belinda            # TTS voice (Phase 5)

# Intent Processing
USE_LLM_FALLBACK=false       # Use LLM for unmatched intents

# Logging
LOG_LEVEL=INFO               # DEBUG, INFO, WARNING, ERROR
```

## Development Phases

### ✅ Phase 1: Core Scaffolding
- Project structure setup
- Basic file organization

### ✅ Phase 2: Boson ASR Integration (CURRENT)
- Audio recording with sounddevice
- WAV file handling (24kHz, mono, 16-bit PCM)
- Boson ASR transcription via OpenAI-compatible API
- Retry logic with exponential backoff
- PTT loop with clean exit handling

### 🔲 Phase 3: Intent Routing
- Rule-based intent matching with regex
- YAML configuration for patterns
- Optional LLM fallback for complex queries

### 🔲 Phase 4: Command Handlers & Dispatcher
- Navigate command (drive to cafeteria)
- Play radio command
- Emergency stop command
- Intent-to-handler registry

### 🔲 Phase 5: TTS Integration
- Boson TTS for voice responses
- Audio playback via ffplay
- Confirmation messages

### 🔲 Phase 6: Device Abstraction
- Simulated car for testing
- Route execution with timing
- Command sequence API

### 🔲 Phase 7+: Physical Hardware
- Serial communication with RC car
- ESP32 firmware integration

## API Reference

### Audio Recording

```python
from app.audio_io import record_ptt

# Record 2.5 seconds at 24kHz
wav_path = record_ptt()
```

### ASR Transcription

```python
from app.boson_api import asr_transcribe

# Transcribe WAV file
transcript = asr_transcribe("path/to/audio.wav")
```

## Troubleshooting

**"BOSON_API_KEY environment variable not set"**
- Copy `.env.example` to `.env` and add your API key

**"Audio recording failed"**
- Check that your microphone is connected and accessible
- Try adjusting `AUDIO_SAMPLE_RATE` in `.env`

**"No module named 'sounddevice'"**
- Run `make install` to install dependencies

**Transcription fails**
- Verify your API key is correct
- Check internet connectivity
- Review logs for specific error messages

## Makefile Commands

```bash
make help      # Show available commands
make install   # Install Python dependencies
make run       # Run the voice assistant
make test      # Run unit tests
make clean     # Clean build artifacts and temp files
```

## Technical Details

### Audio Format
- **Sample Rate:** 24kHz (Boson recommended)
- **Channels:** Mono
- **Encoding:** 16-bit PCM
- **Format:** WAV

### API Integration
- **Endpoint:** `https://hackathon.boson.ai/v1`
- **ASR Model:** `higgs-audio-understanding-Hackathon`
- **Method:** OpenAI-compatible `/v1/chat/completions`
- **Retry Strategy:** 3 attempts with exponential backoff (2-10s)

## Contributing

This is an MVP project following a phased development approach. Each phase builds incrementally on the previous one.

## License

MIT License - See LICENSE file for details
