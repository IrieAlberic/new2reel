import streamlit as st
import pandas as pd
from src.managers.user_manager import UserManager

def render_analytics_tab():
    st.markdown("### Performance Analytics")
    
    user_manager = UserManager()
    stats = user_manager.get_stats()
    history = user_manager.get_history()
    
    # Date Range
    col1, col2 = st.columns([3, 1])
    with col1:
        st.selectbox("Time Period", ["Last 7 Days", "Last 30 Days", "Last 3 Months", "All Time"])
    with col2:
        st.button("Export Report")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Metrics
    # Calculate Real Storage
    import os
    total_size = 0
    if os.path.exists("assets"):
        for path, dirs, files in os.walk("assets"):
            for f in files:
                fp = os.path.join(path, f)
                total_size += os.path.getsize(fp)
    
    storage_mb = f"{total_size / (1024*1024):.2f} MB"

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Videos", stats['generated'])
    with c2:
        st.metric("Total Projects", stats['projects'])
    with c3:
        st.metric("Engagement Rate", "N/A")
    with c4:
        st.metric("Storage Used", storage_mb)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts
    if history:
        df = pd.DataFrame(history)
        if 'date' in df.columns:
            st.markdown("**Video Generation Activity**")
            # Mock chart logic if needed based on real data
            st.bar_chart(df['date'])
            
        st.markdown("**Detailed History**")
        st.dataframe(
            df[['title', 'date', 'duration', 'path']],
            use_container_width=True
        )
    else:
        st.info("No data available.")
