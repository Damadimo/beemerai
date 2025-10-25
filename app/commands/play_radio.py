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
    
    Starts background radio playback that continues until stopped.
    
    Args:
        intent: Intent object
        car: Car device interface (unused for radio)
    """
    logger.info(f"📻 Radio command: Play music/radio")
    
    # Get the radio player
    player = get_radio_player()
    
    # Start playing the default station
    success = player.play()
    
    if success:
        station = player.get_current_station()
        logger.info(f"   Now playing: {station}")
        logger.info(f"   Radio will play in background")
        
        return {
            "status": "acknowledged",
            "action": "play_radio",
            "message": f"Tuning in to {station}. Enjoy the music!"
        }
    else:
        logger.error("   Failed to start radio")
        return {
            "status": "error",
            "action": "play_radio",
            "message": "Sorry, I'm having trouble with the radio right now."
        }
