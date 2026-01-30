from src.generators.script_gen import GeminiScriptGenerator, OpenAIScriptGenerator, PollinationsScriptGenerator, OpenRouterScriptGenerator
from src.generators.audio_gen import EdgeTTSGenerator, OpenAITTSGenerator
from src.generators.image_gen import PollinationsImageGenerator, Dalle3ImageGenerator
from src.editor import VideoEditor
from src.utils.scraper import fetch_content_from_url
from src.utils.cleaner import clean_script_for_audio
import asyncio
import os

class ContentPipeline:
    def __init__(self, mode="Free"):
        self.mode = mode
        self.script_gen = None
        self.audio_gen = None
        self.image_gen = None
        self.editor = VideoEditor()
        self._initialize_generators()

    def _initialize_generators(self):
        if self.mode == "Free":
            self.script_gen = PollinationsScriptGenerator()
            self.audio_gen = EdgeTTSGenerator()
            self.image_gen = PollinationsImageGenerator()
        else:
            # Premium defaults (can be overridden via update_settings)
            # This is a basic init, real keys come from UI
            pass

    def update_settings(self, settings):
        """Re-init generators based on settings dict"""
        # Script
        if settings.get('script_provider') == "OpenAI":
            self.script_gen = OpenAIScriptGenerator(api_key=settings['openai_key'])
        elif settings.get('script_provider') == "Gemini":
            self.script_gen = GeminiScriptGenerator(api_key=settings['gemini_key'])
        elif settings.get('script_provider') == "OpenRouter":
            self.script_gen = OpenRouterScriptGenerator(api_key=settings['openrouter_key'])
        else:
            self.script_gen = PollinationsScriptGenerator()

        # Audio
        if settings.get('audio_provider') == "OpenAI TTS":
            self.audio_gen = OpenAITTSGenerator(api_key=settings['openai_key'])
        else:
            self.audio_gen = EdgeTTSGenerator()

        # Image
        if settings.get('image_provider') == "DALL-E 3":
            self.image_gen = Dalle3ImageGenerator(api_key=settings['openai_key'])
        else:
            self.image_gen = PollinationsImageGenerator()

    async def run(self, topic, language, tone, voice, style, duration="30s", aspect_ratio="9:16 (Shorts)", bg_music=None, subtitles=False, status_callback=None):
        """
        Orchestrates the full generation flow.
        status_callback: function(label, state, progress)
        """
        try:
            # 0. Pre-processing (URL Handling)
            if topic.startswith("http"):
                if status_callback: status_callback("🔗 Fetching URL content...", "running", 5)
                # Fetch content
                scraped_text = fetch_content_from_url(topic)
                if "Error" in scraped_text:
                    raise Exception(scraped_text)
                # Summarize/Pre-process prompt
                pipeline_topic = f"Summarize this content for a video: {scraped_text}"
            else:
                pipeline_topic = topic

            if status_callback:
                status_callback("Generating Script...", "running", 10)
                
            script = self.script_gen.generate(topic, tone, language, duration)
            if "Error" in script: raise Exception(script)
            
            if status_callback:
                status_callback("Generating Audio...", "running", 40)
            
            clean_text = clean_script_for_audio(script)
            audio_path = await self.audio_gen.generate(clean_text, voice)
            
            if "Error" in audio_path: raise Exception(audio_path)
            
            if status_callback:
                status_callback("Generating Visuals...", "running", 70)
            
            # Determine number of images based on duration
            # Simple heuristic: 1 image per 5-10 seconds? 
            # Or better: let's generate 1 image per 100 characters of text?
            # For now, let's just stick to duration tiers as a proxy.
            if "30" in duration:
                num_images = 3
            elif "60" in duration:
                num_images = 5
            elif "90" in duration:
                num_images = 8
            else:
                num_images = 3
                
            # Generate prompts for each image (conceptually)
            # For now, we'll just re-use the topic + style for diversity or split the script?
            # Splitting script is better, but complex.
            # Let's just generate N variations of the topic/style.
            
            image_paths = []
            for i in range(num_images):
                if status_callback:
                    status_callback(f"Generating Image {i+1}/{num_images}...", "running", 70 + int(20 * (i/num_images)))
                
                # Add some variation to prompt
                scene_prompt = f"{topic}, scene {i+1}, visual storytelling" 
                image_path = self.image_gen.generate(prompt=scene_prompt, style=style, aspect_ratio=aspect_ratio)
                
                if "Error" not in image_path:
                    image_paths.append(image_path)
                else:
                    print(f"Image gen error: {image_path}")
            
            if not image_paths:
                raise Exception("Failed to generate any images")
                
            if status_callback:
                status_callback("Editing Video...", "running", 90)
                
            # Ensure unique output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_video = f"output_{timestamp}.mp4"
            
            video_path = self.editor.create_video(
                audio_path, 
                image_paths, 
                output_path=output_video,
                bg_music=bg_music,
                aspect_ratio=aspect_ratio,
                subtitles=subtitles
            )
            
            if status_callback: status_callback("✅ Done!", "complete", 100)
            return {
                "video_path": video_path,
                "script": script,
                "audio_path": audio_path,
                "image_paths": image_paths
            }

        except Exception as e:
            if status_callback: status_callback("❌ Failed", "error", 0)
            raise e
