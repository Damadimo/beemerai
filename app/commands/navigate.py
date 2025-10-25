"""
Navigation Command Handler
Handles navigation requests to destinations.
"""

import logging

logger = logging.getLogger(__name__)


def handle(intent, car):
    """
    Handle navigation intent - drive to a destination.
    
    For MVP, we only support "cafeteria" destination.
    In Phase 6, this will execute actual car movements.
    
    Args:
        intent: Intent object with destination in slots
        car: Car device interface (Phase 6)
    """
    destination = intent.slots.get("destination", "unknown")
    
    logger.info(f"🚗 Navigation command: Going to {destination}")
    
    if destination == "cafeteria":
        # Phase 6 will use: car.sequence(ROUTES["cafeteria"])
        logger.info(f"   Route: Start → Cafeteria")
        logger.info(f"   Status: Route loaded (simulator mode)")
        logger.info(f"   Action: Will execute route in Phase 6")
    else:
        logger.warning(f"   Unknown destination: {destination}")
        logger.info(f"   Available destinations: cafeteria")
    
    return {
        "status": "acknowledged",
        "destination": destination,
        "message": f"Heading to the {destination}"
    }
