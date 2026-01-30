import streamlit as st
from src.managers.template_manager import TemplateManager

def render_templates_tab():
    st.markdown("### Video Templates")
    st.caption("Speed up your workflow with pre-configured templates")
    
    template_manager = TemplateManager()
    all_templates = template_manager.get_templates()
    
    # Categories
    category = st.radio(
        "Category",
        ["All", "News", "Education", "Marketing", "Social Media", "Tutorials"],
        horizontal=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if category != "All":
        templates = [t for t in all_templates if t['category'] == category]
    else:
        templates = all_templates
    
    cols = st.columns(3)
    for idx, template in enumerate(templates):
        with cols[idx % 3]:
            with st.container():
                st.markdown(f"""
                <div style="border: 1px solid rgba(139, 92, 246, 0.2); border-radius: 12px; padding: 1rem; background: rgba(255, 255, 255, 0.03); margin-bottom: 1rem;">
                    <h4>{template['name']}</h4>
                    <p style="color: #9CA3AF; font-size: 0.8rem;">{template['category']} • {template['duration']}</p>
                    <span style="background: rgba(139, 92, 246, 0.2); color: #c4b5fd; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem;">{template['style']}</span>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Use", key=f"use_{idx}", use_container_width=True):
                        st.session_state['create_defaults'] = {
                            'category': template['category'], # content mapping
                            'duration': template.get('duration', '30 sec'),
                            'style': template.get('style', 'Cinematic'),
                            'tone': template.get('tone', 'Professional')
                        }
                        st.toast(f"Applied template: {template['name']}! Go to Create tab.")
                with c2:
                    if st.button("Preview", key=f"prev_{idx}", use_container_width=True):
                        st.info("Previewing style...")
