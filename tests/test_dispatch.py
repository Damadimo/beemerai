"""
Test Command Dispatcher
Unit tests for command dispatching.
"""

import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.intents import Intent
from app.dispatcher import dispatch


def test_navigate_dispatch():
    """Test navigation command dispatch."""
    intent = Intent(
        name="NAVIGATE",
        slots={"destination": "cafeteria"},
        raw_text="take me to the cafeteria"
    )
    
    result = dispatch(intent)
    assert result["status"] == "acknowledged"
    assert result["destination"] == "cafeteria"
    assert "cafeteria" in result["message"].lower()


def test_play_radio_dispatch():
    """Test radio command dispatch."""
    intent = Intent(
        name="PLAY_RADIO",
        slots={},
        raw_text="play the radio"
    )
    
    result = dispatch(intent)
    assert result["status"] == "acknowledged"
    assert result["action"] == "play_radio"


def test_estop_dispatch():
    """Test emergency stop command dispatch."""
    intent = Intent(
        name="ESTOP",
        slots={},
        raw_text="stop"
    )
    
    result = dispatch(intent)
    assert result["status"] == "acknowledged"
    assert result["action"] == "estop"


def test_help_dispatch():
    """Test help command dispatch."""
    intent = Intent(
        name="HELP",
        slots={},
        raw_text="help"
    )
    
    result = dispatch(intent)
    assert result["status"] == "acknowledged"
    assert "cafeteria" in result["message"].lower()
    assert "radio" in result["message"].lower()


def test_unknown_dispatch():
    """Test unknown command dispatch."""
    intent = Intent(
        name="UNKNOWN",
        slots={},
        confidence=0.0,
        raw_text="this makes no sense"
    )
    
    result = dispatch(intent)
    assert result["status"] == "unknown"
    assert "help" in result["message"].lower()


if __name__ == "__main__":
    print("Running dispatcher tests...")
    
    test_navigate_dispatch()
    print("✓ Navigate dispatch tests passed")
    
    test_play_radio_dispatch()
    print("✓ Play radio dispatch tests passed")
    
    test_estop_dispatch()
    print("✓ Emergency stop dispatch tests passed")
    
    test_help_dispatch()
    print("✓ Help dispatch tests passed")
    
    test_unknown_dispatch()
    print("✓ Unknown dispatch tests passed")
    
    print("\nAll dispatcher tests passed! ✓")
