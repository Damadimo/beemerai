"""
Emergency Stop Command Handler
Handles emergency stop requests.
"""

import logging

logger = logging.getLogger(__name__)


def handle(intent, car):
    """
    Handle emergency stop intent - immediately halt all movement.
    
    This is the highest priority safety command.
    Phase 6 will call car.estop() to actually stop the car.
    
    Args:
        intent: Intent object
        car: Car device interface (Phase 6)
    """
    logger.warning(f"🛑 EMERGENCY STOP activated!")
    logger.warning(f"   Status: All movement halted")
    logger.warning(f"   Action: car.estop() will be called in Phase 6")
    
    # Phase 6 will use: car.estop()
    
    return {
        "status": "acknowledged",
        "action": "estop",
        "message": "Emergency stop activated"
    }
