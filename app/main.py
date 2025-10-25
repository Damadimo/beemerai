"""
AI Car Main Application
Voice-controlled car assistant with push-to-talk interface.
"""

import logging
from dotenv import load_dotenv

from app.logging_cfg import setup_logging
from app.audio_io import record_ptt, play_audio
from app.boson_api import asr_transcribe, tts_speak, tts_speak_custom_voice
from app.intents import match_intent
from app.dispatcher import dispatch
from app.radio_player import get_radio_player

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
    
    # Get radio player
    radio = get_radio_player()
    
    try:
        while True:
            # Wait for push-to-talk (Enter key)
            input()
            logger.info("PTT activated - starting recording...")
            
            # Pause radio during recording if playing
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
                result = dispatch(intent, car=None)  # car will be added in Phase 6
                logger.info(f"RESULT: {result.get('message', 'No message')}")
                
                # Speak response (Phase 5)
                response_text = result.get('message', '')
                use_custom_voice = result.get('use_custom_voice', False)
                
                if response_text:
                    try:
                        # Use custom voice for conversations, simple TTS for commands
                        if use_custom_voice:
                            logger.info("Using custom voice for conversational response")
                            tts_path = tts_speak_custom_voice(response_text)
                        else:
                            tts_path = tts_speak(response_text)
                        
                        # Play TTS response (blocking - waits until speech finishes)
                        play_audio(tts_path)
                    except Exception as e:
                        logger.error(f"TTS/playback failed: {e}")
                
                # Resume radio AFTER TTS finishes (if it was playing before)
                if radio_was_playing:
                    logger.info("Resuming radio playback...")
                    radio.play()
                
                logger.info("")
            except Exception as e:
                logger.error(f"Processing failed: {e}")
                # Resume radio even if processing failed
                if radio_was_playing:
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
        
        logger.info("=" * 60)


if __name__ == "__main__":
    main()
