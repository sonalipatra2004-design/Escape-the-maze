import streamlit as st
from datetime import date

def check_daily_reward():
    today = str(date.today())
    return today != st.session_state.get('last_reward_date', '')

def show_home():
    st.markdown("""
    <style>
    .home-title {
        text-align: center;
        font-size: 3em;
        font-weight: bold;
        color: #0066cc;
    }
    </style>
    <div class="home-title">🌀 AI MAZE</div>
    <p style='text-align:center; color:#555; font-size:1.1em;'>
    Every maze is unique. Can you escape?</p>
    """, unsafe_allow_html=True)

    # Daily reward notification
    if check_daily_reward():
        st.warning("🎁 Daily Reward Available! Click below to claim!")

    # First time player
    if st.session_state.get('games_played', 0) == 0:
        st.info("👋 New here? Click 📖 Tutorial to learn how to play!")

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("▶  PLAY NOW",
                     use_container_width=True, type="primary"):
            st.session_state.screen   = 'game'
            st.session_state.new_game = True
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("📖  Tutorial",
                     use_container_width=True):
            st.session_state.tutorial_step = 0
            st.session_state.screen        = 'tutorial'
            st.rerun()

        if st.button("❓  How To Play",
                     use_container_width=True):
            st.session_state.screen = 'guide'
            st.rerun()

        if st.button("🎁  Daily Reward",
                     use_container_width=True):
            st.session_state.screen = 'daily_reward'
            st.rerun()

        if st.button("🎯  Missions",
                     use_container_width=True):
            st.session_state.screen = 'missions'
            st.rerun()

        if st.button("🏅  Achievements",
                     use_container_width=True):
            st.session_state.screen = 'achievements'
            st.rerun()

        if st.button("📊  Statistics",
                     use_container_width=True):
            st.session_state.screen = 'statistics'
            st.rerun()

        if st.button("🏆  Leaderboard",
                     use_container_width=True):
            st.session_state.screen = 'leaderboard'
            st.rerun()

        if st.button("🛒  Shop",
                     use_container_width=True):
            st.session_state.screen = 'shop'
            st.rerun()

        if st.button("👤  Profile",
                     use_container_width=True):
            st.session_state.screen = 'profile'
            st.rerun()

        if st.button("⚙️  Settings",
                     use_container_width=True):
            st.session_state.screen = 'settings'
            st.rerun()

    st.markdown("---")

    # Stats bar
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🪙 Coins",  st.session_state.get('coins', 0))
    c2.metric("💎 Gems",   st.session_state.get('gems', 0))
    c3.metric("🏆 Wins",   st.session_state.get('wins', 0))
    c4.metric("⬆️ Level",  st.session_state.get('player_level', 1))
