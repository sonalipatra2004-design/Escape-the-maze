from screens.seasonal import show_seasonal_settings
import streamlit as st

def show_settings():
    st.title("⚙️ Settings")

    st.subheader("🎮 Gameplay")
    diff = st.slider("Difficulty Level", 1, 5,
                     st.session_state.get('difficulty', 1))
    st.session_state.difficulty = diff
    st.caption("1 = Easy (small maze, few enemies) → 5 = Expert (huge maze, smart enemies)")

    maze_size = st.select_slider(
        "Maze Size",
        options=['Small', 'Medium', 'Large', 'Huge'],
        value=st.session_state.get('maze_size', 'Medium'))
    st.session_state.maze_size = maze_size

    st.markdown("---")
    st.subheader("🎨 Appearance")
    dark_mode = st.toggle("Dark Mode",
                           value=st.session_state.get('dark_mode', True))
    st.session_state.dark_mode = dark_mode
   
    theme = st.selectbox("Default Maze Theme",
                         ['Space', 'Forest', 'Desert', 'Ice', 'Lava', 'Haunted'],
                         index=0)
    st.session_state.theme = theme

    st.markdown("---")
    show_seasonal_settings()
    
    st.markdown("---")
    st.subheader("♿ Accessibility")
    colorblind = st.toggle("Color-blind Mode",
                            value=st.session_state.get('colorblind', False))
    st.session_state.colorblind = colorblind

    large_ui = st.toggle("Large Controls (easier tapping)",
                          value=st.session_state.get('large_ui', False))
    st.session_state.large_ui = large_ui

    st.markdown("---")
    st.subheader("🔔 Notifications")
    st.toggle("Daily Reward Reminder", value=True)
    st.toggle("New High Score Alert",  value=True)
    st.toggle("Weekly Challenge Alert",value=True)

    st.markdown("---")
    if st.button("💾 Save Settings", type="primary", use_container_width=True):
        st.success("✅ All settings saved!")

    if st.button("🏠 Back to Home", use_container_width=True):
        st.session_state.screen = 'home'
        st.rerun()
