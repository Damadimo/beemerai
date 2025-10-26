"""
Command Dispatcher
Routes intents to their command handlers and executes them.
"""

import logging
from app.intents import Intent
from app.intents.fallback_llm import chat_with_car
from app.commands import navigate, play_radio, pause_radio, dance, estop

logger = logging.getLogger(__name__)


# Map intent names to their handler functions
INTENT_HANDLERS = {
    "NAVIGATE": navigate.handle,
    "PLAY_RADIO": play_radio.handle,
    "PAUSE_RADIO": pause_radio.handle,
    "DANCE": dance.handle,
    "ESTOP": estop.handle,
}


def dispatch(intent: Intent, car=None) -> dict:
    """
    Dispatch an intent to its appropriate command handler.
    
    Args:
        intent: Intent object from intent matching
        car: Car device interface (optional, for Phase 6)
    
    Returns:
        dict: Result from the handler with status and message
    """
    intent_name = intent.name
    
    logger.info(f"Dispatching intent: {intent_name}")
    
    # Handle HELP intent specially
    if intent_name == "HELP":
        return handle_help()
    
    # Handle UNKNOWN intent
    if intent_name == "UNKNOWN":
        return handle_unknown(intent)
    
    # Get the handler for this intent
    handler = INTENT_HANDLERS.get(intent_name)
    
    if handler is None:
        logger.error(f"No handler registered for intent: {intent_name}")
        return {
            "status": "error",
            "message": f"No handler for {intent_name}"
        }
    
    # Execute the handler
    try:
        result = handler(intent, car)
        logger.info(f"Handler completed: {result.get('status', 'unknown')}")
        return result
    except Exception as e:
        logger.error(f"Handler failed: {e}")
        return {
            "status": "error",
            "message": f"Command failed: {str(e)}"
        }


def handle_help() -> dict:
    """
    Handle HELP intent - show available commands.
    
    Returns:
        dict: Help information
    """
    logger.info(f"ℹ️  Help requested")
    logger.info(f"   Available commands:")
    logger.info(f"   - 'Take me to the cafeteria' → Navigate to cafeteria")
    logger.info(f"   - 'Play the radio' → Start music playback")
    logger.info(f"   - 'Pause' → Stop the radio")
    logger.info(f"   - 'Stop' → Emergency stop")
    
    return {
        "status": "acknowledged",
        "message": "I can drive to the cafeteria, play the radio, or chat with you. What would you like?"
    }


def handle_unknown(intent: Intent) -> dict:
    """
    Handle UNKNOWN intent - have a conversation with the car.
    
    Uses LLM to generate natural conversational responses.
    Uses simple TTS (not custom voice) for reliability.
    
    Args:
        intent: Intent object with raw text
    
    Returns:
        dict: Conversation response
    """
    logger.info(f"💬 Conversational input: '{intent.raw_text}'")
    
    # Use LLM to generate a natural response
    try:
        car_response = chat_with_car(intent.raw_text)
        logger.info(f"   Car says: '{car_response}'")
        
        return {
            "status": "conversation",
            "message": car_response
        }
    except Exception as e:
        logger.error(f"Conversation failed: {e}")
        return {
            "status": "error",
            "message": "Sorry, I'm having trouble thinking right now."
        }
