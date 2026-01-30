from abc import ABC, abstractmethod

class ScriptGenerator(ABC):
    @abstractmethod
    def generate(self, topic: str, tone: str = "Viral", language: str = "English") -> str:
        """Generate a video script from a topic with specific tone and language."""
        pass

class AudioGenerator(ABC):
    @abstractmethod
    async def generate(self, text: str, voice: str) -> str:
        """Generate audio from text using a specific voice code."""
        pass

class ImageGenerator(ABC):
    @abstractmethod
    def generate(self, prompt: str, style: str = "Cinematic") -> str:
        """Generate an image from a prompt with a specific style."""
        pass
