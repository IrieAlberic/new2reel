from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, TextClip, concatenate_videoclips, CompositeAudioClip
import moviepy.audio.fx.all as afx
import os

class VideoEditor:
    def create_video(self, audio_path: str, image_paths: list, output_path: str = "output_reel.mp4", bg_music: str = None, aspect_ratio: str = "9:16 (Shorts)", subtitles: bool = False) -> str:
        """
        Combines audio and multiple images into a video.
        image_paths: str (single) or list of str
        """
        try:
            # Normalize input
            if isinstance(image_paths, str):
                image_paths = [image_paths]

            # Load Main Audio (Voiceover)
            voice_clip = AudioFileClip(audio_path)
            total_duration = voice_clip.duration
            
            # Calculate duration per image
            if not image_paths:
                raise ValueError("No images provided")
                
            clip_duration = total_duration / len(image_paths)
            
            clips = []
            for img_path in image_paths:
                clip = ImageClip(img_path).set_duration(clip_duration)
                
                # Apply Ken Burns Zoom Effect (Subtle Zoom In)
                # Zoom from 1.0 to 1.05 over the duration
                clip = clip.resize(lambda t: 1 + 0.02 * t)  
                
                # Resize to target aspect ratio (centering)
                # Note: 'resize' with logic above preserves aspect but scales.
                # To enforce 9:16 or 16:9 strictly requires cropping, which we can add later.
                # For now, we trust the generator's aspect ratio + this zoom.
                
                clips.append(clip)
            
            # Concatenate Visuals
            final_video = concatenate_videoclips(clips, method="compose")
            
            # --- Audio Mixing ---
            audio_tracks = [voice_clip]
            
            if bg_music and bg_music != "None":
                music_file = os.path.join("assets", "music", f"{bg_music.lower()}.mp3")
                if os.path.exists(music_file):
                    music_clip = AudioFileClip(music_file)
                    
                    # Loop music if shorter, or trim if longer
                    if music_clip.duration < total_duration:
                        music_clip = afx.audio_loop(music_clip, duration=total_duration)
                    else:
                        music_clip = music_clip.subclip(0, total_duration)
                        
                    # Lower volume
                    music_clip = music_clip.volumex(0.15)
                    audio_tracks.append(music_clip)
                else:
                    print(f"Warning: Music file not found at {music_file}")
            
            # Composite Audio
            final_audio = CompositeAudioClip(audio_tracks)
            final_video = final_video.set_audio(final_audio)
            
            # --- Subtitles (Placeholder) ---
            if subtitles:
                # TODO: Implement subtitle generation via EdgeTTS word timestamps
                pass

            # Write file
            final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
            
            return output_path
            
        except Exception as e:
            return f"Video Editor Error: {str(e)}"
