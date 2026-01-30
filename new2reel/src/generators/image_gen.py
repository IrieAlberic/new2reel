import os
import requests
from openai import OpenAI
from .base import ImageGenerator
import urllib.parse

class PollinationsImageGenerator(ImageGenerator):
    def generate(self, prompt: str, style: str = "Cinematic", aspect_ratio: str = "9:16 (Shorts)") -> str:
        # Determine dimensions based on aspect ratio
        if "9:16" in aspect_ratio:
            width, height = 720, 1280
            orientation_prompt = "vertical"
        elif "16:9" in aspect_ratio:
            width, height = 1280, 720
            orientation_prompt = "wide, horizontal"
        else:
            width, height = 1024, 1024
            orientation_prompt = "square"

        final_prompt = f"{style} style: {prompt}, high quality, 8k, {orientation_prompt}"
        encoded_prompt = urllib.parse.quote(final_prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true"
        
        # Unique filename to avoid overwrites (optional, but good practice)
        import uuid
        filename = f"image_pollinations_{uuid.uuid4().hex[:6]}.jpg"
        output_file = os.path.join("assets", filename)
        os.makedirs("assets", exist_ok=True)
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                return output_file
            else:
                return f"Pollinations Error: Status {response.status_code}"
        except Exception as e:
            return f"Pollinations Error: {str(e)}"

class Dalle3ImageGenerator(ImageGenerator):
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def generate(self, prompt: str, style: str = "Cinematic", aspect_ratio: str = "9:16 (Shorts)") -> str:
        if not self.client:
            return "Error: Missing OpenAI API Key."
            
        final_prompt = f"{style} style: {prompt}. High quality, detailed."
        
        # DALL-E 3 supported sizes
        if "16:9" in aspect_ratio:
            size_param = "1792x1024"
        elif "9:16" in aspect_ratio:
            size_param = "1024x1792"
        else:
            size_param = "1024x1024"

        import uuid
        filename = f"image_dalle3_{uuid.uuid4().hex[:6]}.png"
        output_file = os.path.join("assets", filename)
        os.makedirs("assets", exist_ok=True)

        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=final_prompt,
                size=size_param,
                quality="standard",
                n=1,
            )
            image_url = response.data[0].url
            
            # Download the image
            img_data = requests.get(image_url).content
            with open(output_file, 'wb') as f:
                f.write(img_data)
                
            return output_file
        except Exception as e:
            return f"DALL-E 3 Error: {str(e)}"
