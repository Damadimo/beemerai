"""
Intents Module
Handles natural language understanding and intent recognition.
"""

from app.intents.types import Intent, IntentName
from app.intents.rules import match_intent, get_rule_engine
from app.intents.registry import get_registry

__all__ = [
    'Intent',
    'IntentName', 
    'match_intent',
    'get_rule_engine',
    'get_registry'
]
