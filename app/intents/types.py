"""
Intent Types
Defines data structures for different types of user intents.
"""

from typing import Literal, Dict, Any
from dataclasses import dataclass


# Define the possible intent names for MVP
IntentName = Literal["NAVIGATE", "PLAY_RADIO", "ESTOP", "HELP", "UNKNOWN"]


@dataclass
class Intent:
    """
    Represents a user intent extracted from speech.
    
    Attributes:
        name: The type of intent (NAVIGATE, PLAY_RADIO, ESTOP, HELP, UNKNOWN)
        slots: Dictionary of extracted parameters (e.g., {"destination": "cafeteria"})
        confidence: Confidence score (1.0 for rule-based, varies for LLM)
        raw_text: Original transcribed text
    """
    name: IntentName
    slots: Dict[str, Any]
    confidence: float = 1.0
    raw_text: str = ""
    
    def __str__(self) -> str:
        """String representation for logging."""
        slots_str = ", ".join(f"{k}={v}" for k, v in self.slots.items()) if self.slots else "none"
        return f"Intent({self.name}, slots=[{slots_str}])"
