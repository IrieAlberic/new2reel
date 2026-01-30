import os
from google import genai
from openai import OpenAI
from .base import ScriptGenerator

class GeminiScriptGenerator(ScriptGenerator):
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.client = None
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
            
    def generate(self, topic: str, tone: str = "Viral", language: str = "English", duration: str = "30s") -> str:
        if not self.client:
            return "Error: Missing Google API Key. Get one at aistudio.google.com"
        
        prompt = f"""
        Write a {tone} {language} script for a short {duration} video about: {topic}.
        Strict Rules:
        1. Language: {language} ONLY. 
        2. Tone: {tone}.
        3. OUTPUT ONLY THE SPOKEN WORDS. NO TITLES. NO MARKDOWN. NO [SCENE DIRECTIONS].
        4. Do not wrap in quotes.
        5. Just the raw text to be spoken by the narrator.
        """
        try:
            response = self.client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Gemini Error: {str(e)}"

class PollinationsScriptGenerator(ScriptGenerator):
    def generate(self, topic: str, tone: str = "Viral", language: str = "English", duration: str = "30s") -> str:
        import requests
        import urllib.parse
        
        prompt = f"""
        Write a {tone} {language} script for a short {duration} video about: {topic}.
        Strict Rules:
        1. Language: {language} ONLY. 
        2. Tone: {tone}.
        3. OUTPUT ONLY THE SPOKEN WORDS. NO TITLES. NO MARKDOWN. NO [SCENE DIRECTIONS].
        4. Do not wrap in quotes.
        5. Just the raw text to be spoken by the narrator.
        """
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://text.pollinations.ai/{encoded_prompt}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                return f"Pollinations Text Error: Status {response.status_code}"
        except Exception as e:
            return f"Pollinations Text Error: {str(e)}"

class OpenAIScriptGenerator(ScriptGenerator):
    def __init__(self, api_key=None, model="gpt-4o"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def generate(self, topic: str, tone: str = "Viral", language: str = "English", duration: str = "30s") -> str:
        if not self.client:
            return "Error: Missing OpenAI API Key."
            
        prompt = f"Write a {tone} {language} script for a short {duration} video about: {topic}. Return ONLY the spoken words. No titles, no markdown, no scene directions."
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI Error: {str(e)}"

class OpenRouterScriptGenerator(OpenAIScriptGenerator):
    def __init__(self, api_key=None, model="google/gemini-2.0-flash-exp:free"):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.model = model
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        ) if self.api_key else None
