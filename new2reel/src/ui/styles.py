import streamlit as st

def apply_custom_css():
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* --- RESET & VARIABLES --- */
    :root {
        --bg-dark: #0B0B12;
        --bg-card: rgba(255, 255, 255, 0.04);
        --border-color: rgba(255, 255, 255, 0.08);
        --primary-glow: #8B5CF6;
        --primary-hover: #A78BFA;
        --text-white: #FFFFFF;
        --text-gray: #B5B5C8;
    }

    /* --- GLOBAL THEME --- */
    .stApp {
        background-color: #0B0B12;
        background-image: 
            radial-gradient(circle at 50% 0%, #141027 0%, #0B0B12 100%),
            url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%238b5cf6' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        color: var(--text-white);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* --- SIDEBAR --- */
    section[data-testid="stSidebar"] {
        background: rgba(11, 11, 18, 0.8) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid var(--border-color);
        box-shadow: 10px 0 30px rgba(0,0,0,0.5);
    }
    
    /* --- GLASS CARDS --- */
    .glass-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        backdrop-filter: blur(16px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-4px);
        border-color: rgba(139, 92, 246, 0.3);
        box-shadow: 0 10px 40px rgba(139, 92, 246, 0.15);
    }
    
    /* --- TYPOGRAPHY --- */
    h1, h2, h3 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: white !important;
        letter-spacing: -0.02em;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #FFFFFF 0%, #B5B5C8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .highlight-text {
        color: #8B5CF6;
        -webkit-text-fill-color: #8B5CF6;
    }

    /* --- BUTTONS & CTAS --- */
    .stButton button {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.8rem 2rem !important;
        border-radius: 9999px !important; /* Pill shape */
        font-weight: 600 !important;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.4) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .stButton button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 0 30px rgba(139, 92, 246, 0.6) !important;
        filter: brightness(1.1);
    }

    /* --- INPUTS --- */
    .stTextInput input, .stTextArea textarea, .stSelectbox select, .stSlider div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2) !important;
        background: rgba(255, 255, 255, 0.08) !important;
    }

    /* --- TABS --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(255, 255, 255, 0.02);
        padding: 0.5rem;
        border-radius: 9999px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 2rem;
        width: fit-content;
        margin-left: auto;
        margin-right: auto;
    }

    .stTabs [data-baseweb="tab"] {
        height: auto;
        padding: 0.5rem 1.5rem;
        border-radius: 9999px;
        color: #8A8AA3;
        font-weight: 500;
        border: none;
        background: transparent;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(139, 92, 246, 0.1);
        color: #A78BFA;
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.2);
    }

    /* --- METRICS --- */
    div[data-testid="stMetricValue"] {
        background: linear-gradient(135deg, #A78BFA 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        font-size: 2rem !important;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #8A8AA3 !important;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 1px;
    }

    /* --- CUSTOM CONTAINERS --- */
    .preview-container {
        background: #000000;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.1);
        padding: 4px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }

    /* HIDE STREAMLIT ELEMENTS */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
