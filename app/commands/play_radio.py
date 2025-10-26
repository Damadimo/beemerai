"""
Play Radio Command Handler
Handles radio and music playback.
"""

import logging
from app.radio_player import get_radio_player

logger = logging.getLogger(__name__)


def handle(intent, car):
    """
    Handle play radio intent - start live radio streaming.
    
    Returns a message first, then radio will be started AFTER TTS in main.py.
    
    Args:
        intent: Intent object
        car: Car device interface (unused for radio)
    """
    logger.info(f"📻 Radio command: Play music/radio")
    logger.info(f"   Radio will start after TTS response")
    
    return {
        "status": "acknowledged",
        "action": "play_radio",
        "start_radio": True,  # Signal to start radio AFTER TTS
        "message": "Tuning in to 92.5 FM. Enjoy the music!"
    }
