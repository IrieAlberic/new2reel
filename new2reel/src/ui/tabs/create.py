import streamlit as st
import asyncio
import time
from datetime import datetime
from src.managers.user_manager import UserManager

def render_create_tab(pipeline):
    col_left, col_right = st.columns([1.2, 1])
    user_manager = UserManager()
    
    # Load defaults from template if set
    defaults = st.session_state.get('create_defaults', {})
    
    # Load defaults from template if set
    defaults = st.session_state.get('create_defaults', {})
    
    with col_left:
        # Content Section
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h3>📝 Content & Script</h3>', unsafe_allow_html=True)
        
        input_method = st.radio(
            "Input Method",
            ["Manual Topic", "URL/Article", "RSS Feed", "Trending Topics"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        if input_method == "Manual Topic":
            topic = st.text_area("Enter your topic", "The future of Artificial Intelligence", height=100)
        elif input_method == "URL/Article":
            topic = st.text_input("Paste article URL")
        elif input_method == "RSS Feed":
            topic = st.text_input("RSS Feed URL")
        else:
            topic = "Trending AI news"
        
        c1, c2, c3 = st.columns(3)
        with c1:
            tone_opts = ["Viral/Hype", "Professional", "Dramatic", "Funny", "Educational"]
            def_tone = defaults.get('tone') if defaults.get('tone') in tone_opts else "Viral/Hype"
            tone = st.selectbox("Tone", tone_opts, index=tone_opts.index(def_tone))
        with c2:
            language = st.selectbox("Language", ["English", "French", "Spanish", "German"])
        with c3:
            dur_opts = ["30 sec", "60 sec", "90 sec", "Custom"]
            def_dur = defaults.get('duration') if defaults.get('duration') in dur_opts else "30 sec"
            duration = st.selectbox("Duration", dur_opts, index=dur_opts.index(def_dur))
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

        # Style Section
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h3>🎨 Visual Style</h3>', unsafe_allow_html=True)
        
        # Audio
        voice_options = {
            "Male (Guy)": "en-US-GuyNeural", 
            "Female (Jenny)": "en-US-JennyNeural"
        } 
        # (Simplified logic for brevity in UI update, keeping it clean)
        selected_voice_name = st.selectbox("Voice Actor", list(voice_options.keys()))
        selected_voice_code = voice_options[selected_voice_name]
        
        style_opts = ["Realistic", "Cinematic", "Cyberpunk", "Anime", "Sketch", "Oil Painting"]
        def_style = defaults.get('style') if defaults.get('style') in style_opts else "Cinematic"
        visual_style = st.select_slider("Art Direction", options=style_opts, value=def_style)
        
        c1, c2 = st.columns(2)
        with c1:
             aspect_ratio = st.selectbox("Format", ["9:16 (Shorts)", "16:9 (YouTube)"])
        with c2:
             bg_music = st.selectbox("Background Music", ["None", "Upbeat", "Chill", "Dramatic", "Cyberpunk"])
             
        subtitles = st.checkbox("Add Subtitles", value=False)
        
        generate_btn = st.button("✨ Generate Video", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)


    # OUTPUT
    with col_right:
        st.markdown("### Live Preview")
        st.markdown('<div class="video-preview-container">', unsafe_allow_html=True)
        
        if generate_btn:
            status_container = st.empty()
            with st.status("Rendering...", expanded=True) as status:
                try:
                    # Callback wrapper to update streamlit UI
                    def update_ui(label, state, progress):
                        status.update(label=label, state=state)
                    
                    # RUN PIPELINE
                    result = asyncio.run(pipeline.run(
                        topic=topic,
                        language=language,
                        tone=tone,
                        voice=selected_voice_code,
                        style=visual_style,
                        duration=duration,
                        aspect_ratio=aspect_ratio,
                        bg_music=bg_music,
                        subtitles=subtitles,
                        status_callback=update_ui
                    ))
                    
                    # Success
                    st.success("Generation Complete!")
                    st.video(result['video_path'])
                    
                    # Save to History
                    user_manager.add_video_to_history(
                        title=topic[:30],
                        path=result['video_path']
                    )
                    
                    with st.expander("View Script"):
                        st.write(result['script'])

                except Exception as e:
                    status.update(label="Generation Failed", state="error")
                    st.error(str(e))
        else:
            st.info("Configure settings on the left to start.")
        
        st.markdown('</div>', unsafe_allow_html=True)
