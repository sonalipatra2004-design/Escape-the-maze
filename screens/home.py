import streamlit as st

def show_home():
    st.markdown("""
    <style>
    .home-title {
        text-align: center;
        font-size: 3em;
        font-weight: bold;
        color: #00FFFF;
        text-shadow: 0 0 20px #00FFFF;
    }
    </style>
    <div class="home-title">🌀 AI MAZE</div>
    <p style='text-align:center; color:#aaa; font-size:1.1em;'>
    Every maze is unique. Can you escape?</p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("▶  PLAY NOW", use_container_width=True, type="primary"):
            st.session_state.screen = 'game'
            st.session_state.new_game = True
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("📖  Story Mode",     use_container_width=True):
            st.session_state.screen = 'game'
            st.session_state.new_game = True
            st.rerun()

        if st.button("♾️  Endless Mode",   use_container_width=True):
            st.session_state.screen = 'game'
            st.session_state.new_game = True
            st.rerun()

        if st.button("⏱️  Time Challenge", use_container_width=True):
            st.session_state.screen = 'game'
            st.session_state.new_game = True
            st.rerun()

        if st.button("🏆  Leaderboard",    use_container_width=True):
            st.session_state.screen = 'leaderboard'
            st.rerun()

        if st.button("🛒  Shop",           use_container_width=True):
            st.session_state.screen = 'shop'
            st.rerun()

        if st.button("👤  Profile",        use_container_width=True):
            st.session_state.screen = 'profile'
            st.rerun()

        if st.button("⚙️  Settings",       use_container_width=True):
            st.session_state.screen = 'settings'
            st.rerun()

    st.markdown("---")
    c1, c2 = st.columns(2)
    c1.metric("🪙 Coins", st.session_state.get('coins', 0))
    c2.metric("💎 Gems",  st.session_state.get('gems', 0))
