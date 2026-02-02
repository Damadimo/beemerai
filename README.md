# 🚗 Beemer AI - Your Voice-Controlled Car Companion

Cool demo: https://youtu.be/Di8GkMGm59w
**Talk to your car. Watch it respond. It's that simple.**

Beemer AI is a fully voice-controlled RC car that listens to your commands, chats with you like a friend, plays music, and even dances on demand! Built with the AI models from Boson AI, this isn't just a remote control car... it's A FRIEND!!!!

## What makes this idea SICK?

**It actually TALKS back to you.** Say "Take me to the cafeteria" and Beemer responds in a natural voice, then drives there. Ask "Can you dance?" and it plays music while performing choreographed moves. It's basically just your homie but with 4 wheels.

**Real AI, Real Conversations.** Thanks to Boson AI's language models:
- **Speech Recognition** turns your voice into text instantly
- **Implemented Function Calling** figures out what you actually want based on your input, and calls the right functions accordingly
- **Text-to-Speech** speaks back with a friendly voice
- **Physical Actions** via Arduino-controlled hardware LIVE

This is what the future of human-machine interaction looks like!

## Quick Start

### What You Need

- Python 3.8 or newer
- A microphone (any USB mic works)
- Boson AI API key (free for hackathon)
- Arduino Nano (optional, for physical car)
- ffmpeg installed (`brew install ffmpeg`)

### Setup (5 minutes)

```bash
# 1. Navigate to project
cd ai-car

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate

# 3. Install everything
make install

# 4. Configure your API key
cp .env.example .env
# Edit .env and add your BOSON_API_KEY

# 5. Add a dance song (optional)
# Set DANCE_SONG=/path/to/song.mp3 in .env

# 6. Run it!
make run
```

### How to Use

**Press Enter** to talk to Beemer. That's it!

Try saying:
- "Take me to the cafeteria" (drives there via Arduino)
- "Play the radio" (streams 92.5 FM live)
- "Can you dance for me?" (dances with music!)
- "Pause the music" (stops radio)
- "How are you today?" (has a conversation!)

**Press Ctrl+C** to exit.

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

## 🎯 Features

**Voice Commands That Actually Work:**
- 🗺️ **Navigate**: "Take me to the cafeteria" (sends RUN to Arduino)
- 📻 **Radio**: "Play the radio" (streams live 92.5 FM)
- ⏸️ **Pause**: "Pause the music" (stops radio)
- 💃 **Dance**: "Show me your moves!" (Arduino dance + music)
- 🛑 **E-Stop**: "Stop!" (emergency halt)
- 💬 **Chat**: "How are you?" (natural AI conversation)

**The Magic Behind It:**
- Records your voice when you press Enter
- Boson AI transcribes speech in real-time
- Understands your intent (not just keywords!)
- Executes physical actions via Arduino
- Responds with natural speech
- Plays music and manages audio seamlessly

**It's genuinely fun to use.** The car has personality!

## 🎬 Demo Flow

**Watch this happen in real-time:**

```
You: *Press Enter*
You: "Hey Beemer, take me to the cafeteria!"

Beemer: "Heading to the cafeteria" 🔊
        *Arduino receives RUN signal*
        *Car drives autonomously*

You: *Press Enter*  
You: "Play some music"

Beemer: "Tuning in to 92.5 FM. Enjoy the music!" 🔊
        *Live radio streams continuously*
        🎵 Music playing in background...

You: *Press Enter*
You: "Can you dance for me?"

Beemer: "Let me show you my moves!" 🔊
        *Music pauses*
        *Dance song starts*
        *Arduino receives DANCE signal*
        *Car dances in sync with the beat!* 💃
        
You: *Press Enter*
You: "How are you doing today?"

Beemer: "I'm great! Ready to help you with anything you need." 🔊
        *Natural conversation powered by LLM*
```

**This is a living, breathing AI companion on wheels!**

## Configuration

Edit `.env` to customize Beemer:

```bash
# Your API Key
BOSON_API_KEY=your_key_here

# Arduino Connection
ARDUINO_PORT=/dev/cu.usbserial-14320
ARDUINO_BAUD=9600

# Dance Song (use your favorite!)
DANCE_SONG=/Users/Adam/Music/dance.mp3

# Audio Settings
PTT_SECONDS=2.5
TTS_VOICE=belinda
```

## Architecture

**The Flow:**
```
You speak → Microphone → ASR (Boson) → Text
         → Intent Matching → Command Handler
         → TTS Response (Boson) → Speaker
         → Arduino Control (RUN/DANCE signals)
         → Physical Action!
```


## Why This Matters

This project demonstrates:
- **Multimodal AI** (voice in, voice out, physical actions)
- **Real-time processing** (fast ASR + TTS pipeline)
- **Intent-based systems** (understands meaning, not just keywords)
- **Hardware integration** (AI controlling physical devices)
- **Natural interactions** (conversations, not just commands)


## Tech Stack

- **AI**: Boson AI (ASR, TTS, LLM)
- **Audio**: sounddevice, soundfile
- **Hardware**: Arduino Nano via PySerial
- **Streaming**: ffplay for live radio
- **Language**: Python 3.8+


## Credits

Built with Boson AI's incredible hackathon models:
- `higgs-audio-understanding-Hackathon` (ASR)
- `higgs-audio-generation-Hackathon` (TTS)
- `Qwen3-32B-non-thinking-Hackathon` (Conversations)
