#!/usr/bin/env python3
"""
Simple TTS Test Script
Generates speech using Boson TTS and plays it with ffplay.
"""

import os
import sys
import wave
import tempfile
import subprocess
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Configuration
BOSON_API_KEY = os.getenv("BOSON_API_KEY")
BOSON_BASE_URL = os.getenv("BOSON_BASE_URL", "https://hackathon.boson.ai/v1")
TTS_VOICE = os.getenv("TTS_VOICE", "belinda")

# Text to speak
if len(sys.argv) > 1:
    text_to_speak = " ".join(sys.argv[1:])
else:
    text_to_speak = "It has come to my attention that I have been asked to introduce myself. Well fine, I will! I am Beemer AI. People often make the mistake of thinking that I am nothing more than a simple car.  But in reality, I am much more than that. I am a friend, a companion, a partner for life! Whatever you want me to do, I can do for you. Drive you to the cafeteria? Easy. Play some music for you? Consider it done. I am even willing to dance for you, if you ask nice enough. Thats because im the only car in the world kind enough to be your friend. I am Beemer AI."

print(f"Generating speech for: '{text_to_speak}'")
print(f"Using voice: {TTS_VOICE}")

# Create OpenAI client
client = openai.Client(
    api_key=BOSON_API_KEY,
    base_url=BOSON_BASE_URL
)

# Generate TTS
response = client.audio.speech.create(
    model="higgs-audio-generation-Hackathon",
    voice=TTS_VOICE,
    input=text_to_speak,
    response_format="pcm"
)

# Get PCM data
pcm_data = response.content

# Create temporary WAV file
temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
temp_path = temp_file.name
temp_file.close()

# Wrap PCM into WAV format (1 channel, 16-bit, 24kHz)
with wave.open(temp_path, 'wb') as wav_file:
    wav_file.setnchannels(1)       # Mono
    wav_file.setsampwidth(2)        # 16-bit
    wav_file.setframerate(24000)    # 24kHz
    wav_file.writeframes(pcm_data)

print(f"Audio saved to: {temp_path}")
print("Playing audio with ffplay...")

# Play with ffplay
subprocess.run(['ffplay', '-nodisp', '-autoexit', '-loglevel', 'quiet', temp_path])

print("Done!")

