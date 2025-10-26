"""
Navigation Command Handler
Handles navigation requests to destinations.
"""

import logging
from app.arduino_client import get_arduino_client

logger = logging.getLogger(__name__)


def handle(intent, car):
    """
    Handle navigation intent - drive to a destination.
    
    For MVP, we only support "cafeteria" destination.
    Sends RUN command to Arduino to execute the route.
    
    Args:
        intent: Intent object with destination in slots
        car: Car device interface (Phase 6)
    """
    destination = intent.slots.get("destination", "unknown")
    
    logger.info(f"🚗 Navigation command: Going to {destination}")
    
    if destination == "cafeteria":
        logger.info(f"   Route: Start → Cafeteria")
        logger.info(f"   Will send RUN command to Arduino after TTS")
        
        return {
            "status": "acknowledged",
            "destination": destination,
            "message": f"Heading to the {destination}",
            "send_arduino_run": True  # Signal to send RUN after TTS
        }
    else:
        logger.warning(f"   Unknown destination: {destination}")
        logger.info(f"   Available destinations: cafeteria")
        
        return {
            "status": "error",
            "destination": destination,
            "message": f"Sorry, I don't know how to get to {destination}"
        }
