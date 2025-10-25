"""
Test Intent Rules
Unit tests for intent matching.
"""

import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.intents import match_intent


def test_navigate_intent():
    """Test navigation intent matching."""
    # Direct mention
    intent = match_intent("take me to the cafeteria")
    assert intent.name == "NAVIGATE"
    assert intent.slots.get("destination") == "cafeteria"
    
    # Variations
    assert match_intent("go to the canteen").name == "NAVIGATE"
    assert match_intent("drive to the food court").name == "NAVIGATE"
    assert match_intent("cafeteria").name == "NAVIGATE"


def test_play_radio_intent():
    """Test radio/music intent matching."""
    intent = match_intent("play something from the radio")
    assert intent.name == "PLAY_RADIO"
    
    # Variations
    assert match_intent("turn on the radio").name == "PLAY_RADIO"
    assert match_intent("play music").name == "PLAY_RADIO"
    assert match_intent("radio").name == "PLAY_RADIO"


def test_estop_intent():
    """Test emergency stop intent matching."""
    intent = match_intent("emergency stop")
    assert intent.name == "ESTOP"
    
    # Variations
    assert match_intent("stop now").name == "ESTOP"
    assert match_intent("stop").name == "ESTOP"
    assert match_intent("e-stop").name == "ESTOP"


def test_help_intent():
    """Test help intent matching."""
    intent = match_intent("help")
    assert intent.name == "HELP"
    
    # Variations
    assert match_intent("what can you do").name == "HELP"
    assert match_intent("commands").name == "HELP"


def test_unknown_intent():
    """Test unknown/unmatched input."""
    intent = match_intent("this is nonsense text that should not match")
    assert intent.name == "UNKNOWN"
    assert intent.confidence == 0.0


def test_intent_priority():
    """Test that ESTOP has priority over other matches."""
    # "stop" should match ESTOP first, not navigate
    intent = match_intent("stop the car")
    assert intent.name == "ESTOP"


if __name__ == "__main__":
    print("Running intent tests...")
    
    test_navigate_intent()
    print("✓ Navigate intent tests passed")
    
    test_play_radio_intent()
    print("✓ Play radio intent tests passed")
    
    test_estop_intent()
    print("✓ Emergency stop intent tests passed")
    
    test_help_intent()
    print("✓ Help intent tests passed")
    
    test_unknown_intent()
    print("✓ Unknown intent tests passed")
    
    test_intent_priority()
    print("✓ Intent priority tests passed")
    
    print("\nAll tests passed! ✓")
