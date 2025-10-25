"""
Audio Input/Output Module
Handles microphone input and speaker output for voice commands.
"""

import os
import tempfile
import logging
import sounddevice as sd
import soundfile as sf

logger = logging.getLogger(__name__)


def record_ptt(seconds: float = None, sample_rate: int = None) -> str:
    """
    Record audio via push-to-talk (PTT) and save to a temporary WAV file.
    
    Records audio from the default microphone in mono format with 16-bit PCM encoding.
    The recording is saved to a temporary file that persists until manually deleted.
    
    Args:
        seconds: Duration to record in seconds (default from PTT_SECONDS env var or 2.5)
        sample_rate: Sample rate in Hz (default from AUDIO_SAMPLE_RATE env var or 24000)
    
    Returns:
        str: Path to the saved WAV file
    
    Raises:
        Exception: If recording fails
    """
    # Get configuration from environment or use defaults
    if seconds is None:
        seconds = float(os.getenv("PTT_SECONDS", "2.5"))
    
    if sample_rate is None:
        sample_rate = int(os.getenv("AUDIO_SAMPLE_RATE", "24000"))
    
    logger.info(f"Recording {seconds}s of audio at {sample_rate}Hz...")
    
    try:
        # Record audio (mono, blocking call)
        # dtype='int16' gives us 16-bit PCM directly
        audio_data = sd.rec(
            int(seconds * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype='int16',
            blocking=True
        )
        
        logger.debug("Recording complete, waiting for device...")
        sd.wait()  # Ensure recording is complete
        
        # Create temporary WAV file
        # delete=False keeps the file after the handle closes
        temp_file = tempfile.NamedTemporaryFile(
            suffix='.wav',
            prefix='ai_car_',
            delete=False
        )
        temp_path = temp_file.name
        temp_file.close()  # Close handle so soundfile can write
        
        # Write audio data to WAV file with proper format
        # subtype='PCM_16' ensures 16-bit PCM encoding
        sf.write(
            temp_path,
            audio_data,
            sample_rate,
            subtype='PCM_16'
        )
        
        logger.info(f"Audio saved to {temp_path}")
        return temp_path
    
    except Exception as e:
        logger.error(f"Audio recording failed: {e}")
        raise


def play_audio(wav_path: str) -> None:
    """
    Play audio from a WAV file.
    
    Uses sounddevice for simple, cross-platform playback.
    Blocks until playback is complete.
    
    Args:
        wav_path: Path to WAV file to play
    """
    try:
        logger.info(f"Playing audio from {wav_path}")
        
        # Read WAV file
        audio_data, sample_rate = sf.read(wav_path)
        
        # Play audio (blocking)
        sd.play(audio_data, sample_rate, blocking=True)
        sd.wait()
        
        logger.debug("Audio playback complete")
    
    except Exception as e:
        logger.error(f"Audio playback failed: {e}")
        raise
