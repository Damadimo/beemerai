"""
Boson API Integration
Handles communication with the Boson AI service for ASR and TTS.
"""

import os
import base64
import logging
import tempfile
import wave
import openai
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def asr_transcribe(wav_path: str) -> str:
    """
    Transcribe a WAV file using Boson's higgs-audio-understanding model.
    
    Args:
        wav_path: Path to WAV file (24kHz, mono, 16-bit PCM recommended)
    
    Returns:
        str: Transcribed text from the audio
    """
    try:
        # Get API credentials
        api_key = os.getenv("BOSON_API_KEY")
        if not api_key:
            raise ValueError("BOSON_API_KEY environment variable not set")
        
        base_url = os.getenv("BOSON_BASE_URL", "https://hackathon.boson.ai/v1")
        
        # Create client (using exact pattern from Boson docs)
        client = openai.Client(
            api_key=api_key,
            base_url=base_url
        )
        
        # Encode audio to base64
        with open(wav_path, "rb") as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")
        
        file_format = wav_path.split(".")[-1]
        
        logger.info(f"Transcribing audio from {wav_path}")
        
        # Call Boson ASR (exact pattern from Boson docs)
        response = client.chat.completions.create(
            model="higgs-audio-understanding-Hackathon",
            messages=[
                {"role": "system", "content": "Transcribe this audio for me."},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_audio",
                            "input_audio": {
                                "data": audio_base64,
                                "format": file_format,
                            },
                        },
                    ],
                },
            ],
            max_completion_tokens=256,
            temperature=0.0,
        )
        
        # Extract transcript
        transcript = response.choices[0].message.content.strip()
        logger.info(f"Transcript received: '{transcript}'")
        
        return transcript
    
    except Exception as e:
        logger.error(f"ASR transcription failed: {str(e)[:100]}")
        raise


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def tts_speak(text: str, voice: str = None) -> str:
    """
    Convert text to speech using Boson's higgs-audio-generation model.
    
    Returns PCM audio data wrapped in a WAV file.
    Uses the simple /audio/speech endpoint as recommended.
    
    Args:
        text: Text to convert to speech
        voice: Voice to use (default from TTS_VOICE env var or "belinda")
    
    Returns:
        str: Path to generated WAV file
    """
    try:
        # Get API credentials
        api_key = os.getenv("BOSON_API_KEY")
        if not api_key:
            raise ValueError("BOSON_API_KEY environment variable not set")
        
        base_url = os.getenv("BOSON_BASE_URL", "https://hackathon.boson.ai/v1")
        
        # Get voice from parameter or environment
        if voice is None:
            voice = os.getenv("TTS_VOICE", "belinda")
        
        # Create client
        client = openai.Client(
            api_key=api_key,
            base_url=base_url
        )
        
        logger.info(f"Generating speech: '{text[:50]}...' (voice: {voice})")
        
        # Call Boson TTS (using /audio/speech endpoint)
        response = client.audio.speech.create(
            model="higgs-audio-generation-Hackathon",
            voice=voice,
            input=text,
            response_format="pcm"
        )
        
        # Get PCM data
        pcm_data = response.content
        
        # Create temporary WAV file
        temp_file = tempfile.NamedTemporaryFile(
            suffix='.wav',
            prefix='tts_',
            delete=False
        )
        temp_path = temp_file.name
        temp_file.close()
        
        # Wrap PCM into WAV format (1 channel, 16-bit, 24kHz as per Boson specs)
        with wave.open(temp_path, 'wb') as wav_file:
            wav_file.setnchannels(1)      # Mono
            wav_file.setsampwidth(2)       # 16-bit
            wav_file.setframerate(24000)   # 24kHz
            wav_file.writeframes(pcm_data)
        
        logger.info(f"TTS audio saved to {temp_path}")
        
        return temp_path
    
    except Exception as e:
        logger.error(f"TTS generation failed: {str(e)[:100]}")
        raise


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def tts_speak_custom_voice(text: str, reference_audio_path: str = None, reference_transcript: str = None) -> str:
    """
    Convert text to speech using custom voice cloning.
    
    Uses Boson's voice cloning via chat completions with reference audio.
    This creates more natural, personalized responses for conversations.
    
    Args:
        text: Text to convert to speech
        reference_audio_path: Path to reference audio WAV (optional, uses default if not provided)
        reference_transcript: Transcript of reference audio (optional, uses default if not provided)
    
    Returns:
        str: Path to generated WAV file
    """
    try:
        # Get API credentials
        api_key = os.getenv("BOSON_API_KEY")
        if not api_key:
            raise ValueError("BOSON_API_KEY environment variable not set")
        
        base_url = os.getenv("BOSON_BASE_URL", "https://hackathon.boson.ai/v1")
        
        # Use default reference if not provided
        # For MVP, we'll use a simple friendly voice profile
        if reference_transcript is None:
            reference_transcript = "[SPEAKER1] Hello! I'm your AI car assistant. I'm here to help you with navigation and entertainment."
        
        # Create client
        client = openai.Client(
            api_key=api_key,
            base_url=base_url
        )
        
        logger.info(f"Generating custom voice speech: '{text[:50]}...'")
        
        # System prompt for natural voice generation
        system_prompt = """You are an AI assistant designed to convert text into speech.
If the user's message includes a [SPEAKER*] tag, do not read out the tag and generate speech for the following text, using the specified voice.
If no speaker tag is present, select a suitable voice on your own.

<|scene_desc_start|>
Audio is recorded from inside a car cabin with minimal background noise.
<|scene_desc_end|>"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": reference_transcript},
        ]
        
        # Add reference audio if provided
        if reference_audio_path and os.path.exists(reference_audio_path):
            with open(reference_audio_path, "rb") as f:
                audio_b64 = base64.b64encode(f.read()).decode("utf-8")
            
            messages.append({
                "role": "assistant",
                "content": [{
                    "type": "input_audio",
                    "input_audio": {"data": audio_b64, "format": "wav"}
                }],
            })
        
        # Add the text to speak
        messages.append({"role": "user", "content": f"[SPEAKER1] {text}"})
        
        # Call Boson custom voice TTS
        response = client.chat.completions.create(
            model="higgs-audio-generation-Hackathon",
            messages=messages,
            modalities=["text", "audio"],
            max_completion_tokens=4096,
            temperature=1.0,
            top_p=0.95,
            stream=False,
            stop=["<|eot_id|>", "<|end_of_text|>", "<|audio_eos|>"],
            extra_body={"top_k": 50}
        )
        
        # Get audio data
        audio_b64 = response.choices[0].message.audio.data
        audio_data = base64.b64decode(audio_b64)
        
        # Save to temporary WAV file
        temp_file = tempfile.NamedTemporaryFile(
            suffix='.wav',
            prefix='tts_custom_',
            delete=False
        )
        temp_path = temp_file.name
        temp_file.write(audio_data)
        temp_file.close()
        
        logger.info(f"Custom voice TTS audio saved to {temp_path}")
        
        return temp_path
    
    except Exception as e:
        logger.error(f"Custom voice TTS failed: {str(e)[:100]}")
        # Fallback to simple TTS
        logger.info("Falling back to simple TTS")
        return tts_speak(text)
