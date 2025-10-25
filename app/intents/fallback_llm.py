"""
Fallback LLM Handler
Uses Boson's LLM for conversational responses when no command is matched.
"""

import os
import logging
import openai

logger = logging.getLogger(__name__)


def chat_with_car(user_message: str) -> str:
    """
    Have a conversation with the car using Boson's LLM.
    
    Uses Qwen3-14B-Hackathon for fast, natural responses.
    The car has a helpful, friendly personality.
    
    Args:
        user_message: User's message to the car
    
    Returns:
        str: Car's response text
    """
    try:
        # Get API credentials
        api_key = os.getenv("BOSON_API_KEY")
        if not api_key:
            raise ValueError("BOSON_API_KEY environment variable not set")
        
        base_url = os.getenv("BOSON_BASE_URL", "https://hackathon.boson.ai/v1")
        
        # Create client
        client = openai.Client(
            api_key=api_key,
            base_url=base_url
        )
        
        # System prompt - define car's personality
        system_prompt = """You are an intelligent AI assistant built into a car. 
You are helpful, friendly, and concise. Keep responses brief (1-2 sentences max).
You can drive to the cafeteria, play the radio, and have conversations.
Be conversational and natural, like a helpful companion on a drive."""
        
        logger.info(f"LLM chat: '{user_message[:50]}...'")
        
        # Use Qwen3-32B-non-thinking for fast responses without thinking tags
        response = client.chat.completions.create(
            model="Qwen3-32B-non-thinking-Hackathon",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=128,
            temperature=0.7
        )
        
        car_response = response.choices[0].message.content.strip()
        
        # Clean up any remaining <think> tags if they somehow appear
        import re
        car_response = re.sub(r'<think>.*?</think>', '', car_response, flags=re.DOTALL).strip()
        
        logger.info(f"LLM response: '{car_response}'")
        
        return car_response
    
    except Exception as e:
        logger.error(f"LLM chat failed: {str(e)[:100]}")
        return "Sorry, I'm having trouble thinking right now. Could you try again?"
