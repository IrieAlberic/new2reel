import os
import edge_tts
from openai import OpenAI
from .base import AudioGenerator

class EdgeTTSGenerator(AudioGenerator):
    def __init__(self, voice="en-US-GuyNeural"):
        self.voice = voice

    async def generate(self, text: str, voice: str = None) -> str:
        """
        Generates audio using Edge TTS (Free).
        Returns the path to the generated file.
        """
        final_voice = voice or self.voice
        output_file = os.path.join("assets", "audio.mp3")
        
        # Ensure assets dir exists
        os.makedirs("assets", exist_ok=True)
        
        try:
            communicate = edge_tts.Communicate(text, final_voice)
            await communicate.save(output_file)
            return output_file
        except Exception as e:
            return f"EdgeTTS Error: {str(e)}"

class OpenAITTSGenerator(AudioGenerator):
    def __init__(self, api_key=None, model="tts-1", voice="alloy"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.default_voice = voice
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    async def generate(self, text: str, voice: str = None) -> str:
        if not self.client:
            return "Error: Missing OpenAI API Key."
            
        final_voice = voice or self.default_voice
        output_file = os.path.join("assets", "audio_openai.mp3")
        os.makedirs("assets", exist_ok=True)

        try:
            response = self.client.audio.speech.create(
                model=self.model,
                voice=final_voice,
                input=text
            )
            response.stream_to_file(output_file)
            return output_file
        except Exception as e:
            return f"OpenAI TTS Error: {str(e)}"
