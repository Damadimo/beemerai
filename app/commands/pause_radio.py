"""
Pause Radio Command Handler
Handles pausing/stopping the radio.
"""

import logging
from app.radio_player import get_radio_player

logger = logging.getLogger(__name__)


def handle(intent, car):
    """
    Handle pause radio intent - stop radio playback.
    
    Note: Radio is already paused by main.py when PTT is activated.
    This handler just acknowledges the pause and prevents auto-resume.
    
    Args:
        intent: Intent object
        car: Car device interface (unused for radio)
    """
    logger.info(f"⏸️  Pause radio command")
    logger.info(f"   Radio will remain paused")
    
    return {
        "status": "acknowledged",
        "action": "pause_radio",
        "message": "Radio paused."
    }

