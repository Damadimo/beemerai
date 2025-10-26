"""
AI Car Main Application
Voice-controlled car assistant with push-to-talk interface.
"""

import os
import logging
import time
import threading
from dotenv import load_dotenv

from app.logging_cfg import setup_logging
from app.audio_io import record_ptt, play_audio, play_local_audio
from app.boson_api import asr_transcribe, tts_speak, tts_speak_custom_voice
from app.intents import match_intent
from app.dispatcher import dispatch
from app.radio_player import get_radio_player
from app.arduino_client import get_arduino_client

# Load environment variables from .env file
load_dotenv()

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)


def main():
    """
    Main application loop for the AI car voice assistant.
    
    Workflow:
    1. Wait for user to press Enter (push-to-talk)
    2. Record audio for configured duration
    3. Transcribe audio using Boson ASR
    4. Log the transcript
    5. Repeat until Ctrl+C
    """
    logger.info("=" * 60)
    logger.info("AI Car Voice Assistant - MVP Complete!")
    logger.info("=" * 60)
    logger.info("Press Enter to start recording, Ctrl+C to exit")
    logger.info("")
    
    # Get radio player and Arduino client
    radio = get_radio_player()
    arduino = get_arduino_client()
    
    try:
        while True:
            # Wait for push-to-talk (Enter key)
            input()
            logger.info("PTT activated - starting recording...")
            
            # Check if radio is playing BEFORE we stop it
            radio_was_playing = radio.is_playing()
            if radio_was_playing:
                logger.info("Pausing radio for voice input...")
                radio.stop()
            
            # Record audio from microphone
            try:
                wav_path = record_ptt()
            except Exception as e:
                logger.error(f"Recording failed: {e}")
                # Resume radio if it was playing
                if radio_was_playing:
                    radio.play()
                continue
            
            # Transcribe the recorded audio
            try:
                transcript = asr_transcribe(wav_path)
                logger.info(f"USER SAID: {transcript}")
                
                # Match intent (Phase 3)
                intent = match_intent(transcript)
                logger.info(f"INTENT: {intent}")
                
                # Dispatch to handler (Phase 4)
                # Pass radio_was_playing state so handlers can see it
                result = dispatch(intent, car=None)  # car will be added in Phase 6
                logger.info(f"RESULT: {result.get('message', 'No message')}")
                
                # Speak response (Phase 5) - always use simple TTS
                response_text = result.get('message', '')
                
                if response_text:
                    try:
                        # Use simple TTS for all responses (faster and more reliable)
                        tts_path = tts_speak(response_text)
                        
                        # Play TTS response (blocking - waits until speech finishes)
                        play_audio(tts_path)
                    except Exception as e:
                        logger.error(f"TTS/playback failed: {e}")
                
                # Handle dance command - start music BEFORE Arduino signal
                if result.get('play_dance_song'):
                    dance_song_path = os.getenv('DANCE_SONG')
                    if dance_song_path and os.path.exists(dance_song_path):
                        logger.info("Starting dance song...")
                        
                        # Start playing song in a non-blocking way
                        def play_song():
                            try:
                                play_local_audio(dance_song_path)
                            except Exception as e:
                                logger.error(f"Dance song playback failed: {e}")
                        
                        song_thread = threading.Thread(target=play_song, daemon=True)
                        song_thread.start()
                        
                        # Give song a moment to start
                        time.sleep(0.5)
                        
                        # NOW send dance signal to Arduino
                        if result.get('send_arduino_dance'):
                            logger.info("Executing dance on Arduino (with music!)...")
                            arduino.send_dance()
                        
                        # Wait for song to finish
                        song_thread.join()
                    else:
                        logger.warning(f"Dance song not found: {dance_song_path}")
                        # Still send dance signal even without music
                        if result.get('send_arduino_dance'):
                            logger.info("Executing dance on Arduino (no music)...")
                            arduino.send_dance()
                
                # Send Arduino RUN command AFTER TTS (for navigation)
                elif result.get('send_arduino_run'):
                    logger.info("Executing navigation on Arduino...")
                    arduino.send_run()
                
                # Handle radio state AFTER TTS finishes
                if result.get('start_radio'):
                    # Start radio for play_radio command
                    logger.info("Starting radio playback now...")
                    radio.play()
                elif intent.name == "PAUSE_RADIO":
                    # Don't resume radio if user wanted to pause it
                    logger.info("Radio remains paused (user requested)")
                elif radio_was_playing:
                    # Resume radio for other commands (conversations, help, etc)
                    logger.info("Resuming radio playback...")
                    radio.play()
                
                logger.info("")
            except Exception as e:
                logger.error(f"Processing failed: {e}")
                # Resume radio even if processing failed (unless it was a pause command)
                if radio_was_playing and intent.name != "PAUSE_RADIO":
                    radio.play()
                logger.info("")
    
    except KeyboardInterrupt:
        logger.info("")
        logger.info("=" * 60)
        logger.info("Shutting down AI Car Voice Assistant")
        
        # Stop radio if playing
        if radio.is_playing():
            logger.info("Stopping radio...")
            radio.stop()
        
        # Disconnect Arduino
        arduino.disconnect()
        
        logger.info("=" * 60)


if __name__ == "__main__":
    main()
