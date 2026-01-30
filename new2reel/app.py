import streamlit as st
from src.ui.styles import apply_custom_css
from src.pipeline import ContentPipeline
from src.ui.tabs import create, projects, analytics, templates
from src.managers.user_manager import UserManager

# --- CONFIG ---
st.set_page_config(
    page_title="News2Reel Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply extracted CSS
apply_custom_css()

# --- INIT ---
if 'pipeline' not in st.session_state:
    st.session_state.pipeline = ContentPipeline(mode="Free")
user_manager = UserManager()

# --- NAVBAR (MOCK) ---
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 1rem 0; margin-bottom: 3rem;">
    <div style="font-weight: 800; font-size: 1.5rem; background: linear-gradient(to right, #8B5CF6, #EC4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">News2Reel</div>
    <div style="display: flex; gap: 2rem; color: #B5B5C8; font-size: 0.9rem;">
        <span>Pricing</span>
        <span>Guide</span>
        <span>Showcase</span>
    </div>
    <div style="color: #8B5CF6; font-weight: 600; cursor: pointer;">Sign In</div>
</div>
""", unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown('<h1 class="hero-title">Fastest & Easiest Way to <br>Generate <span class="highlight-text">Short Videos</span></h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #8A8AA3; font-size: 1.2rem; margin-bottom: 3rem;">Turn text into viral content in seconds with our next-gen AI engine.</p>', unsafe_allow_html=True)

# --- MAIN DEMO INTERFACE ---
# We wrap the tabs in a glass container visually
with st.container():
    tab_create, tab_projects, tab_templates, tab_analytics = st.tabs([
        "Create Video", 
        "My Projects", 
        "Templates",
        "Analytics"
    ])

    with tab_create:
        create.render_create_tab(st.session_state.pipeline)

    with tab_projects:
        projects.render_projects_tab()
        
    with tab_templates:
        templates.render_templates_tab()
        
    with tab_analytics:
        analytics.render_analytics_tab()

# --- FEATURES / SOCIAL PROOF ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown('<h3 style="text-align: center; margin-bottom: 2rem;">Powerful tool for boosting social media growth</h3>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="glass-card">
        <h3 style="margin:0;">🚀 AI Speed</h3>
        <p style="color: #8A8AA3;">Generate full videos in under 60 seconds.</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="glass-card">
        <h3 style="margin:0;">🎙️ Natural Voice</h3>
        <p style="color: #8A8AA3;">Ultra-realistic TTS with emotion control.</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="glass-card">
        <h3 style="margin:0;">🎨 Auto-Visuals</h3>
        <p style="color: #8A8AA3;">Context-aware image generation.</p>
    </div>
    """, unsafe_allow_html=True)
