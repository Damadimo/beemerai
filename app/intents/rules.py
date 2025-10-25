"""
Intent Rules Engine
Loads rules from YAML and matches text to intents using regex patterns.
"""

import re
import logging
import yaml
from pathlib import Path
from typing import Optional, List, Dict, Any

from app.intents.types import Intent, IntentName

logger = logging.getLogger(__name__)


class RuleEngine:
    """
    Rule-based intent matcher using regex patterns from YAML configuration.
    """
    
    def __init__(self, rules_path: Optional[str] = None):
        """
        Initialize the rule engine and load rules from YAML.
        
        Args:
            rules_path: Path to rules.yaml file (defaults to same directory)
        """
        if rules_path is None:
            # Default to rules.yaml in the same directory as this file
            rules_path = Path(__file__).parent / "rules.yaml"
        
        self.rules = self._load_rules(rules_path)
        logger.info(f"Loaded {len(self.rules)} intent rules")
    
    def _load_rules(self, rules_path: Path) -> List[Dict[str, Any]]:
        """
        Load intent rules from YAML file.
        
        Args:
            rules_path: Path to YAML rules file
        
        Returns:
            List of rule dictionaries
        """
        try:
            with open(rules_path, 'r') as f:
                config = yaml.safe_load(f)
            return config.get('intents', [])
        except Exception as e:
            logger.error(f"Failed to load rules from {rules_path}: {e}")
            return []
    
    def match(self, text: str) -> Intent:
        """
        Match input text against rules to extract intent.
        
        Rules are evaluated in order. First matching rule wins.
        Returns UNKNOWN intent if no rules match.
        
        Args:
            text: Input text to match (typically from ASR)
        
        Returns:
            Intent object with name and extracted slots
        """
        # Normalize text for matching
        normalized_text = text.lower().strip()
        
        logger.debug(f"Matching text: '{normalized_text}'")
        
        # Try each rule in order
        for rule in self.rules:
            intent_name = rule.get('name')
            patterns = rule.get('patterns', [])
            default_slots = rule.get('slots', {})
            
            # Try each pattern for this intent
            for pattern in patterns:
                try:
                    if re.search(pattern, normalized_text, re.IGNORECASE):
                        # Match found!
                        logger.info(f"Matched intent: {intent_name} (pattern: {pattern[:50]}...)")
                        
                        return Intent(
                            name=intent_name,
                            slots=default_slots.copy(),
                            confidence=1.0,
                            raw_text=text
                        )
                except re.error as e:
                    logger.error(f"Invalid regex pattern '{pattern}': {e}")
        
        # No match found
        logger.warning(f"No intent matched for: '{text}'")
        return Intent(
            name="UNKNOWN",
            slots={},
            confidence=0.0,
            raw_text=text
        )


# Global rule engine instance
_rule_engine: Optional[RuleEngine] = None


def get_rule_engine() -> RuleEngine:
    """
    Get or create the global rule engine instance.
    
    Returns:
        RuleEngine instance
    """
    global _rule_engine
    if _rule_engine is None:
        _rule_engine = RuleEngine()
    return _rule_engine


def match_intent(text: str) -> Intent:
    """
    Convenience function to match text to intent using the global rule engine.
    
    Args:
        text: Input text to match
    
    Returns:
        Intent object
    """
    engine = get_rule_engine()
    return engine.match(text)
