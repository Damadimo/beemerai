"""
Dance Command Handler
Handles dance performance requests.
"""

import logging
from app.arduino_client import get_arduino_client

logger = logging.getLogger(__name__)


def handle(intent, car):
    """
    Handle dance intent - make the car perform a dance routine.
    
    Sends DANCE command to Arduino and plays dance song.
    
    Args:
        intent: Intent object
        car: Car device interface (unused)
    """
    logger.info(f"💃 Dance command activated!")
    logger.info(f"   Will send DANCE signal to Arduino after TTS")
    logger.info(f"   Will play dance song from DANCE_SONG env variable")
    
    return {
        "status": "acknowledged",
        "action": "dance",
        "message": "Let me show you my moves!",
        "send_arduino_dance": True,  # Signal to send DANCE to Arduino
        "play_dance_song": True  # Signal to play dance music
    }

