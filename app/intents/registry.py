"""
Intent Registry
Maps intent names to their handler functions (for Phase 4).
"""

import logging
from typing import Dict, Callable, Any

logger = logging.getLogger(__name__)


# Type alias for intent handler functions
IntentHandler = Callable[[Any, Any], None]


class IntentRegistry:
    """
    Registry that maps intent names to their handler functions.
    
    Handlers will be registered in Phase 4 when we implement commands.
    """
    
    def __init__(self):
        """Initialize empty registry."""
        self._handlers: Dict[str, IntentHandler] = {}
    
    def register(self, intent_name: str, handler: IntentHandler) -> None:
        """
        Register a handler function for an intent.
        
        Args:
            intent_name: Name of the intent (e.g., "NAVIGATE")
            handler: Function to handle this intent
        """
        self._handlers[intent_name] = handler
        logger.info(f"Registered handler for intent: {intent_name}")
    
    def get_handler(self, intent_name: str) -> IntentHandler:
        """
        Get the handler function for an intent.
        
        Args:
            intent_name: Name of the intent
        
        Returns:
            Handler function, or None if not registered
        """
        return self._handlers.get(intent_name)
    
    def has_handler(self, intent_name: str) -> bool:
        """
        Check if a handler is registered for an intent.
        
        Args:
            intent_name: Name of the intent
        
        Returns:
            True if handler exists
        """
        return intent_name in self._handlers
    
    def list_intents(self) -> list:
        """
        Get list of all registered intent names.
        
        Returns:
            List of intent names
        """
        return list(self._handlers.keys())


# Global registry instance
_registry: IntentRegistry = None


def get_registry() -> IntentRegistry:
    """
    Get or create the global intent registry.
    
    Returns:
        IntentRegistry instance
    """
    global _registry
    if _registry is None:
        _registry = IntentRegistry()
    return _registry
