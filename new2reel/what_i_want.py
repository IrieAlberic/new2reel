import streamlit as st
import os
import asyncio
import time
from datetime import datetime, timedelta
from src.generators.script_gen import GeminiScriptGenerator, OpenAIScriptGenerator, OpenRouterScriptGenerator, PollinationsScriptGenerator
from src.generators.audio_gen import EdgeTTSGenerator, OpenAITTSGenerator
from src.generators.image_gen import PollinationsImageGenerator, Dalle3ImageGenerator
from src.editor import VideoEditor

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="News2Reel Studio - AI Video Platform",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INITIALIZE SESSION STATE ---
if 'user_tier' not in st.session_state:
    st.session_state.user_tier = 'Free'
if 'videos_generated' not in st.session_state:
    st.session_state.videos_generated = 0
if 'credits_remaining' not in st.session_state:
    st.session_state.credits_remaining = 10
if 'video_history' not in st.session_state:
    st.session_state.video_history = []
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'templates' not in st.session_state:
    st.session_state.templates = []
if 'current_project' not in st.session_state:
    st.session_state.current_project = None

# --- MODERN SAAS CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Theme */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        color: #E8EAED;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Sidebar Modern Design */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f3a 0%, #0f1225 100%);
        border-right: 1px solid rgba(139, 92, 246, 0.1);
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.3);
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }
    
    /* Logo & Branding */
    .logo-container {
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 2rem;
        border-bottom: 1px solid rgba(139, 92, 246, 0.2);
    }
    
    .logo-text {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }
    
    .logo-subtitle {
        font-size: 0.75rem;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 0.25rem;
    }
    
    /* Navigation Tabs */
    .nav-tabs {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 2rem;
        padding: 0.5rem;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        border: 1px solid rgba(139, 92, 246, 0.1);
    }
    
    .nav-tab {
        flex: 1;
        padding: 0.75rem 1rem;
        background: transparent;
        border: none;
        color: #9CA3AF;
        font-weight: 500;
        font-size: 0.9rem;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .nav-tab.active {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
    }
    
    /* Cards */
    .feature-card {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(236, 72, 153, 0.05) 100%);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(139, 92, 246, 0.2);
        border-color: rgba(139, 92, 246, 0.4);
    }
    
    .stat-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-label {
        font-size: 0.875rem;
        color: #9CA3AF;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.875rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 14px rgba(139, 92, 246, 0.4) !important;
        width: 100%;
    }
    
    .stButton button:hover {
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.6) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Secondary Button */
    .secondary-btn {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        color: #8B5CF6 !important;
    }
    
    /* Input Fields */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(139, 92, 246, 0.2) !important;
        border-radius: 8px !important;
        color: #E8EAED !important;
        padding: 0.75rem !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1) !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(139, 92, 246, 0.15) !important;
        border-radius: 10px !important;
        color: #E8EAED !important;
        font-weight: 600 !important;
        padding: 1rem 1.25rem !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(139, 92, 246, 0.1) !important;
        border-color: rgba(139, 92, 246, 0.3) !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #8B5CF6 0%, #EC4899 100%) !important;
    }
    
    /* Metrics */
    div[data-testid="stMetricValue"] {
        color: #8B5CF6 !important;
        font-size: 1.75rem !important;
        font-weight: 700 !important;
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.375rem 0.875rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .badge-pro {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: white;
    }
    
    .badge-free {
        background: rgba(148, 163, 184, 0.2);
        color: #94A3B8;
    }
    
    .badge-enterprise {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
        color: white;
    }
    
    /* Status Messages */
    .stSuccess {
        background: rgba(34, 197, 94, 0.1) !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
        border-radius: 8px !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 8px !important;
    }
    
    .stWarning {
        background: rgba(251, 191, 36, 0.1) !important;
        border: 1px solid rgba(251, 191, 36, 0.3) !important;
        border-radius: 8px !important;
    }
    
    /* Video Preview */
    .video-preview-container {
        border: 2px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    
    /* Timeline */
    .timeline-item {
        padding: 1rem;
        border-left: 2px solid #8B5CF6;
        margin-left: 1rem;
        margin-bottom: 1rem;
        position: relative;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -6px;
        top: 1.25rem;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #8B5CF6;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(139, 92, 246, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(139, 92, 246, 0.7);
    }
    
    /* Tabs Enhancement */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        color: #9CA3AF;
        font-weight: 600;
        padding: 1rem 0;
    }
    
    .stTabs [aria-selected="true"] {
        color: #8B5CF6;
        border-bottom: 2px solid #8B5CF6;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    # Logo
    st.markdown("""
        <div class="logo-container">
            <div class="logo-text">🎬 News2Reel</div>
            <div class="logo-subtitle">Studio</div>
        </div>
    """, unsafe_allow_html=True)
    
    # User Profile Section
    st.markdown("### 👤 Account")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<span class="badge badge-{st.session_state.user_tier.lower()}">{st.session_state.user_tier}</span>', unsafe_allow_html=True)
    with col2:
        if st.button("⚡ Upgrade"):
            st.session_state.show_pricing = True
    
    # Credits & Usage
    st.markdown("---")
    st.markdown("### 💳 Credits & Usage")
    progress_val = st.session_state.credits_remaining / 10
    st.progress(progress_val)
    st.caption(f"{st.session_state.credits_remaining}/10 credits remaining")
    st.caption(f"🎥 {st.session_state.videos_generated} videos generated this month")
    
    # Quick Actions
    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")
    if st.button("📁 My Projects", use_container_width=True):
        st.session_state.active_tab = "projects"
    if st.button("⭐ Templates", use_container_width=True):
        st.session_state.active_tab = "templates"
    if st.button("📊 Analytics", use_container_width=True):
        st.session_state.active_tab = "analytics"
    
    # Settings Expander
    st.markdown("---")
    with st.expander("⚙️ Engine Settings"):
        provider_mode = st.radio(
            "Compute Engine",
            ["Free Tier (Pollinations/Edge)", "Premium (API Keys)"],
            label_visibility="collapsed"
        )
        
        script_gen = None
        audio_gen = None
        image_gen = None
        
        if "Free" in provider_mode:
            st.success("🟢 Free Engine Active")
            script_gen = PollinationsScriptGenerator()
            audio_gen = EdgeTTSGenerator(voice="en-US-GuyNeural")
            image_gen = PollinationsImageGenerator()
        else:
            openai_key = st.text_input("OpenAI API Key", type="password")
            
            script_provider = st.selectbox("Script Engine", ["OpenAI GPT-4", "OpenRouter", "Gemini"])
            if script_provider == "OpenAI GPT-4":
                script_gen = OpenAIScriptGenerator(api_key=openai_key)
            elif script_provider == "OpenRouter":
                or_key = st.text_input("OpenRouter Key", type="password")
                script_gen = OpenRouterScriptGenerator(api_key=or_key)
            else:
                gem_key = st.text_input("Google API Key", type="password")
                script_gen = GeminiScriptGenerator(api_key=gem_key)
            
            audio_provider = st.selectbox("Voice Engine", ["Edge TTS", "OpenAI TTS"])
            audio_gen = OpenAITTSGenerator(api_key=openai_key) if audio_provider == "OpenAI TTS" else EdgeTTSGenerator()
            
            image_provider = st.selectbox("Visual Engine", ["Pollinations", "DALL-E 3"])
            image_gen = Dalle3ImageGenerator(api_key=openai_key) if image_provider == "DALL-E 3" else PollinationsImageGenerator()
    
    # Help & Support
    st.markdown("---")
    st.markdown("### 💬 Support")
    if st.button("📚 Documentation", use_container_width=True):
        st.info("Documentation opening...")
    if st.button("🎓 Tutorials", use_container_width=True):
        st.info("Tutorials opening...")
    if st.button("💌 Contact Support", use_container_width=True):
        st.info("Support chat opening...")

# --- MAIN CONTENT AREA ---

# Header with Stats
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
        <div class="stat-card">
            <div class="stat-value">""" + str(st.session_state.videos_generated) + """</div>
            <div class="stat-label">Videos Created</div>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div class="stat-card">
            <div class="stat-value">""" + str(st.session_state.credits_remaining) + """</div>
            <div class="stat-label">Credits Left</div>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
        <div class="stat-card">
            <div class="stat-value">""" + str(len(st.session_state.video_history)) + """</div>
            <div class="stat-label">Projects</div>
        </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
        <div class="stat-card">
            <div class="stat-value">5.2K</div>
            <div class="stat-label">Total Views</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Navigation Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎬 Create Video",
    "📁 My Projects",
    "⭐ Templates",
    "📊 Analytics",
    "💎 Upgrade"
])

# ===== TAB 1: CREATE VIDEO =====
with tab1:
    col_left, col_right = st.columns([1.2, 1])
    
    with col_left:
        st.markdown("### 🎨 Video Configuration")
        
        # Content Input Card
        with st.expander("📝 Content & Script", expanded=True):
            input_method = st.radio(
                "Input Method",
                ["Manual Topic", "URL/Article", "RSS Feed", "Trending Topics"],
                horizontal=True
            )
            
            if input_method == "Manual Topic":
                topic = st.text_area(
                    "Enter your topic or description",
                    "The future of Artificial Intelligence in healthcare",
                    height=120
                )
            elif input_method == "URL/Article":
                topic = st.text_input("Paste article URL")
                st.caption("We'll extract and summarize the content automatically")
            elif input_method == "RSS Feed":
                topic = st.text_input("RSS Feed URL")
                st.caption("Generate videos from latest feed items")
            else:
                st.info("🔥 Trending topics feature coming soon!")
                topic = "Trending AI news"
            
            col1, col2, col3 = st.columns(3)
            with col1:
                tone = st.selectbox(
                    "Tone",
                    ["Viral/Hype", "Professional", "Dramatic", "Funny", "Educational", "Inspirational", "News Report"]
                )
            with col2:
                language = st.selectbox(
                    "Language",
                    ["English", "French", "Spanish", "German", "Italian", "Portuguese"]
                )
            with col3:
                video_length = st.selectbox(
                    "Duration",
                    ["30 sec", "60 sec", "90 sec", "2 min", "3 min", "Custom"]
                )
        
        # Voice & Audio Card
        with st.expander("🎙️ Voice & Audio Settings", expanded=True):
            # Dynamic Voice Selection
            voice_options = {}
            if language == "French":
                voice_options = {
                    "Male (Remy)": "fr-FR-RemyMultilingualNeural",
                    "Female (Vivienne)": "fr-FR-VivienneMultilingualNeural",
                    "Male (Henri)": "fr-FR-HenriNeural"
                }
            elif language == "Spanish":
                voice_options = {
                    "Male (Alvaro)": "es-ES-AlvaroNeural",
                    "Female (Elvira)": "es-ES-ElviraNeural"
                }
            elif language == "German":
                voice_options = {
                    "Male (Killian)": "de-DE-KillianNeural",
                    "Female (Katja)": "de-DE-KatjaNeural"
                }
            else:
                voice_options = {
                    "Male (Guy)": "en-US-GuyNeural",
                    "Female (Jenny)": "en-US-JennyNeural",
                    "Male (Christopher)": "en-US-ChristopherNeural"
                }
            
            selected_voice_name = st.selectbox("Voice Actor", list(voice_options.keys()))
            selected_voice_code = voice_options[selected_voice_name]
            
            col1, col2 = st.columns(2)
            with col1:
                bg_music = st.selectbox(
                    "Background Music",
                    ["None", "Upbeat", "Dramatic", "Calm", "Epic", "Corporate", "Custom Upload"]
                )
            with col2:
                music_volume = st.slider("Music Volume", 0, 100, 20, help="Volume of background music")
        
        # Visual Style Card
        with st.expander("🎨 Visual Design", expanded=True):
            visual_style = st.select_slider(
                "Art Direction",
                options=["Realistic", "Cinematic", "Cyberpunk", "Anime", "Sketch", "Oil Painting", "3D Render", "Minimalist"],
                value="Cinematic"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                aspect_ratio = st.selectbox(
                    "Aspect Ratio",
                    ["16:9 (YouTube)", "9:16 (TikTok/Reels)", "1:1 (Instagram)", "4:5 (Feed)"]
                )
            with col2:
                quality = st.selectbox(
                    "Quality",
                    ["Standard (720p)", "HD (1080p)", "Ultra HD (4K)"]
                )
            
            transitions = st.multiselect(
                "Transitions",
                ["Fade", "Zoom", "Slide", "Dissolve", "Glitch", "Wipe"],
                default=["Fade"]
            )
        
        # Advanced Options
        with st.expander("⚙️ Advanced Options"):
            col1, col2 = st.columns(2)
            with col1:
                add_subtitles = st.checkbox("Add Subtitles", value=True)
                add_logo = st.checkbox("Add Watermark/Logo")
            with col2:
                auto_captions = st.checkbox("Auto-generated Captions", value=True)
                color_grade = st.checkbox("Auto Color Grading")
            
            custom_branding = st.text_input("Custom Branding Text (optional)")
        
        # Action Buttons
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            generate_btn = st.button("🚀 Generate Video", use_container_width=True)
        with col2:
            if st.button("💾 Save Draft", use_container_width=True):
                st.success("Draft saved!")
        with col3:
            if st.button("🔄 Reset", use_container_width=True):
                st.rerun()
    
    with col_right:
        st.markdown("### 📺 Live Preview")
        
        # Preview Container
        st.markdown('<div class="video-preview-container">', unsafe_allow_html=True)
        
        if not generate_btn:
            st.info("🎬 Configure your video settings and click 'Generate Video' to start")
            st.markdown("""
                **Quick Tips:**
                - Use trending topics for viral content
                - Add subtitles for better engagement
                - Choose aspect ratio based on platform
                - Background music increases watch time
            """)
            
            # Mock Preview Stats
            st.markdown("---")
            st.markdown("**Estimated Metrics:**")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Processing Time", "~45 sec")
                st.metric("File Size", "~12 MB")
            with col2:
                st.metric("Credits Cost", "1 credit")
                st.metric("Est. Engagement", "High")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Recent Activity
        st.markdown("---")
        st.markdown("### 📊 Recent Activity")
        if st.session_state.video_history:
            for video in st.session_state.video_history[-3:]:
                st.markdown(f"**{video['title']}**")
                st.caption(f"Created {video['date']} • {video['views']} views")
        else:
            st.caption("No videos created yet. Start by generating your first video!")

# ===== EXECUTION LOGIC =====
if generate_btn:
    if not script_gen:
        st.error("⚠️ Configuration Error: Please check API keys in settings")
    elif st.session_state.credits_remaining <= 0:
        st.error("⚠️ No credits remaining. Please upgrade your plan!")
    else:
        with col_right:
            st.markdown('<div class="video-preview-container">', unsafe_allow_html=True)
            
            with st.status("🎬 Rendering your video...", expanded=True) as status:
                try:
                    # Progress tracking
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # 1. Script Generation
                    status_text.write("🤖 AI Script Agent: Analyzing topic...")
                    progress_bar.progress(15)
                    time.sleep(1)
                    
                    script = script_gen.generate(topic, tone=tone, language=language)
                    if "Error" in script:
                        status.update(label="❌ Generation Failed", state="error")
                        st.error(script)
                        st.stop()
                    
                    status_text.write("✅ Script generated successfully")
                    progress_bar.progress(35)
                    
                    # 2. Audio Synthesis
                    status_text.write(f"🎙️ Voice Synthesis: {selected_voice_name}...")
                    time.sleep(1)
                    
                    if isinstance(audio_gen, EdgeTTSGenerator):
                        audio_path = asyncio.run(audio_gen.generate(script, voice=selected_voice_code))
                    else:
                        audio_path = asyncio.run(audio_gen.generate(script, voice=selected_voice_code))
                    
                    if "Error" in audio_path:
                        status.update(label="❌ Audio Failed", state="error")
                        st.error(audio_path)
                        st.stop()
                    
                    status_text.write("✅ Audio synthesized")
                    progress_bar.progress(55)
                    
                    # 3. Visual Generation
                    status_text.write(f"🎨 Visual Engine: Rendering {visual_style} assets...")
                    time.sleep(1.5)
                    
                    image_prompt = f"{visual_style} shot representing: {topic}, highly detailed, professional"
                    image_path = image_gen.generate(image_prompt, style=visual_style)
                    
                    if "Error" in image_path:
                        status.update(label="❌ Visual Generation Failed", state="error")
                        st.error(image_path)
                        st.stop()
                    
                    status_text.write("✅ Visuals rendered")
                    progress_bar.progress(75)
                    
                    # 4. Video Compilation
                    status_text.write("🎬 Final Render: Compiling video with transitions...")
                    time.sleep(2)
                    
                    editor = VideoEditor()
                    output_video = "final_output.mp4"
                    video_path = editor.create_video(audio_path, image_path, output_path=output_video)
                    
                    if "Error" in video_path:
                        status.update(label="❌ Render Failed", state="error")
                        st.error(video_path)
                    else:
                        progress_bar.progress(100)
                        status.update(label="✅ Video Ready!", state="complete")
                        
                        # Update session state
                        st.session_state.videos_generated += 1
                        st.session_state.credits_remaining -= 1
                        st.session_state.video_history.append({
                            'title': topic[:50],
                            'date': datetime.now().strftime("%Y-%m-%d"),
                            'views': 0,
                            'path': video_path
                        })
                        
                        st.success("🎉 Video generated successfully!")
                        st.video(video_path)
                        
                        # Action buttons
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.download_button(
                                "⬇️ Download",
                                data=open(video_path, 'rb'),
                                file_name="news2reel_video.mp4",
                                mime="video/mp4",
                                use_container_width=True
                            )
                        with col2:
                            if st.button("📤 Share", use_container_width=True):
                                st.info("Share dialog opening...")
                        with col3:
                            if st.button("⭐ Save", use_container_width=True):
                                st.success("Added to favorites!")
                        
                        # Show script
                        with st.expander("📝 View Generated Script"):
                            st.text_area("Script", script, height=200)
                        
                        # Analytics mock
                        with st.expander("📊 Video Analytics"):
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Duration", f"{video_length}")
                            with col2:
                                st.metric("File Size", "12.4 MB")
                            with col3:
                                st.metric("Quality", quality)
                
                except Exception as e:
                    status.update(label="❌ System Error", state="error")
                    st.error(f"Critical failure: {str(e)}")
            
            st.markdown('</div>', unsafe_allow_html=True)

# ===== TAB 2: MY PROJECTS =====
with tab2:
    st.markdown("### 📁 My Projects")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        filter_status = st.selectbox("Status", ["All", "Published", "Draft", "Processing"])
    with col2:
        filter_date = st.selectbox("Date", ["All Time", "Today", "This Week", "This Month"])
    with col3:
        sort_by = st.selectbox("Sort By", ["Recent", "Most Viewed", "Title A-Z"])
    with col4:
        st.text_input("🔍 Search projects...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.session_state.video_history:
        for idx, video in enumerate(st.session_state.video_history):
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.markdown(f"**🎬 {video['title']}**")
                    st.caption(f"Created: {video['date']} • Views: {video['views']}")
                with col2:
                    st.markdown('<span class="badge badge-free">Published</span>', unsafe_allow_html=True)
                with col3:
                    if st.button("⋮", key=f"menu_{idx}"):
                        st.info("Actions: Edit, Delete, Duplicate, Share")
                st.markdown("---")
    else:
        st.info("📭 No projects yet. Create your first video in the 'Create Video' tab!")
        if st.button("🎬 Create First Video"):
            st.session_state.active_tab = "create"

# ===== TAB 3: TEMPLATES =====
with tab3:
    st.markdown("### ⭐ Video Templates")
    st.caption("Speed up your workflow with pre-configured templates")
    
    # Template Categories
    template_categories = st.radio(
        "Category",
        ["All", "News", "Education", "Marketing", "Social Media", "Tutorials"],
        horizontal=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Mock Templates
    templates = [
        {"name": "Tech News Brief", "category": "News", "duration": "60 sec", "style": "Professional"},
        {"name": "Product Explainer", "category": "Marketing", "duration": "90 sec", "style": "Modern"},
        {"name": "Tutorial Quick Tip", "category": "Education", "duration": "45 sec", "style": "Friendly"},
        {"name": "Instagram Reel", "category": "Social Media", "duration": "30 sec", "style": "Viral"},
        {"name": "YouTube Intro", "category": "Marketing", "duration": "15 sec", "style": "Cinematic"},
        {"name": "Breaking News", "category": "News", "duration": "2 min", "style": "Dramatic"}
    ]
    
    cols = st.columns(3)
    for idx, template in enumerate(templates):
        with cols[idx % 3]:
            with st.container():
                st.markdown(f"**{template['name']}**")
                st.caption(f"{template['category']} • {template['duration']}")
                st.caption(f"Style: {template['style']}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Use", key=f"use_{idx}", use_container_width=True):
                        st.success(f"Template '{template['name']}' loaded!")
                with col2:
                    if st.button("Preview", key=f"prev_{idx}", use_container_width=True):
                        st.info("Preview opening...")
                st.markdown("---")

# ===== TAB 4: ANALYTICS =====
with tab4:
    st.markdown("### 📊 Performance Analytics")
    
    # Date Range Selector
    col1, col2 = st.columns([3, 1])
    with col1:
        date_range = st.selectbox(
            "Time Period",
            ["Last 7 Days", "Last 30 Days", "Last 3 Months", "All Time"]
        )
    with col2:
        if st.button("📥 Export Report"):
            st.success("Report exported!")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Overview Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Views", "5,234", delta="+12.5%")
    with col2:
        st.metric("Avg Watch Time", "42 sec", delta="+8.2%")
    with col3:
        st.metric("Engagement Rate", "68%", delta="+5.1%")
    with col4:
        st.metric("Total Shares", "892", delta="+23.4%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts (Mock)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**📈 Views Over Time**")
        st.line_chart([10, 25, 45, 60, 85, 120, 145])
    
    with col2:
        st.markdown("**🎯 Top Performing Videos**")
        st.bar_chart({"Video 1": 450, "Video 2": 380, "Video 3": 290, "Video 4": 210})
    
    # Detailed Table
    st.markdown("---")
    st.markdown("**📋 Detailed Performance**")
    import pandas as pd
    mock_data = pd.DataFrame({
        'Video Title': ['AI in Healthcare', 'Climate Change', 'Tech Trends', 'Space Exploration'],
        'Views': [1234, 987, 756, 543],
        'Likes': [234, 189, 145, 98],
        'Shares': [45, 32, 28, 19],
        'Engagement': ['72%', '68%', '65%', '61%']
    })
    st.dataframe(mock_data, use_container_width=True)

# ===== TAB 5: UPGRADE/PRICING =====
with tab5:
    st.markdown("### 💎 Upgrade Your Plan")
    st.caption("Unlock more features and credits")
    
    # Pricing Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <h3>🆓 Free</h3>
                <h2>$0<span style="font-size: 1rem;">/month</span></h2>
                <ul style="list-style: none; padding: 0;">
                    <li>✅ 10 videos/month</li>
                    <li>✅ 720p quality</li>
                    <li>✅ Basic templates</li>
                    <li>✅ Watermark included</li>
                    <li>❌ No priority support</li>
                    <li>❌ Limited styles</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        st.button("Current Plan", disabled=True, use_container_width=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card">
                <h3>⭐ Pro</h3>
                <h2>$29<span style="font-size: 1rem;">/month</span></h2>
                <ul style="list-style: none; padding: 0;">
                    <li>✅ 100 videos/month</li>
                    <li>✅ 1080p HD quality</li>
                    <li>✅ All templates</li>
                    <li>✅ No watermark</li>
                    <li>✅ Priority support</li>
                    <li>✅ Advanced styles</li>
                    <li>✅ Custom branding</li>
                    <li>✅ API access</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Upgrade to Pro", use_container_width=True):
            st.balloons()
            st.success("🎉 Welcome to Pro! Redirecting to payment...")
    
    with col3:
        st.markdown("""
            <div class="feature-card">
                <h3>🚀 Enterprise</h3>
                <h2>Custom</h2>
                <ul style="list-style: none; padding: 0;">
                    <li>✅ Unlimited videos</li>
                    <li>✅ 4K Ultra HD</li>
                    <li>✅ Custom templates</li>
                    <li>✅ White label</li>
                    <li>✅ Dedicated support</li>
                    <li>✅ Team collaboration</li>
                    <li>✅ Advanced analytics</li>
                    <li>✅ SLA guarantee</li>
                    <li>✅ Custom integrations</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Contact Sales", use_container_width=True):
            st.info("📧 Sales team will contact you within 24 hours")
    
    # Feature Comparison Table
    st.markdown("---")
    st.markdown("### 📋 Detailed Feature Comparison")
    
    comparison_df = pd.DataFrame({
        'Feature': [
            'Videos per month', 'Max resolution', 'Templates', 'Watermark',
            'Background music', 'Custom branding', 'Priority rendering',
            'API access', 'Team seats', 'Storage', 'Support'
        ],
        'Free': [
            '10', '720p', 'Basic (5)', '✓ Yes',
            '❌', '❌', '❌', '❌', '1', '1 GB', 'Email'
        ],
        'Pro': [
            '100', '1080p', 'All (50+)', '❌ No',
            '✅', '✅', '✅', '✅', '5', '50 GB', 'Priority'
        ],
        'Enterprise': [
            'Unlimited', '4K', 'Custom', '❌ No',
            '✅', '✅', '✅', '✅', 'Unlimited', 'Unlimited', 'Dedicated'
        ]
    })
    
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
footer_cols = st.columns([2, 1, 1, 1])
with footer_cols[0]:
    st.caption("© 2024 News2Reel Studio. All rights reserved.")
with footer_cols[1]:
    st.caption("[Privacy Policy](#)")
with footer_cols[2]:
    st.caption("[Terms of Service](#)")
with footer_cols[3]:
    st.caption("[API Docs](#)")