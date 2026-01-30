import streamlit as st
from src.managers.user_manager import UserManager

def render_projects_tab():
    st.markdown("### My Projects")
    
    user_manager = UserManager()
    history = user_manager.get_history()
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.selectbox("Status", ["All", "Published", "Draft", "Processing"])
    with col2:
        st.selectbox("Date", ["All Time", "Today", "This Week", "This Month"])
    with col3:
        st.selectbox("Sort By", ["Recent", "Most Viewed", "Title A-Z"])
    with col4:
        st.text_input("Search projects...")
    
    st.markdown("---")
    
    if not history:
        st.info("No projects found. Create your first video!")
        return
    
    for video in history:
        with st.container():
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1:
                st.markdown(f"**{video['title']}**")
                st.caption(f"Date: {video['date']} | Duration: {video.get('duration', '30s')}")
            with c2:
                st.markdown('<span class="badge badge-free">Saved</span>', unsafe_allow_html=True)
            with c3:
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("Play", key=f"play_{video['id']}"):
                        st.video(video['path'])
                with col_btn2:
                    if st.button("Delete", key=f"del_{video['id']}"):
                        user_manager.delete_video(video['id']) 
                        st.toast("Project deleted!", icon=None)
                        st.rerun()
            st.divider()
