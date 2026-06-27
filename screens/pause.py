import streamlit as st

def show_pause():
    st.title("⏸️ Game Paused")
    st.markdown("---")

    st.markdown("""
    <div style='text-align:center; font-size:4em;'>⏸️</div>
    <h2 style='text-align:center;'>Game Paused</h2>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Current game stats while paused
    st.subheader("📊 Current Game Stats")
    player = st.session_state.get('player', None)
    if player:
        c1, c2, c3 = st.columns(3)
        c1.metric("❤️ Lives",  player.lives)
        c2.metric("🪙 Coins",  player.coins)
        c3.metric("🎯 Moves",
                  st.session_state.get('move_count', 0))

    st.markdown("---")

    col1, col2 = st.columns(2)

    if col1.button("▶️ Resume Game",
                   use_container_width=True,
                   type="primary"):
        st.session_state.screen = 'game'
        st.rerun()

    if col2.button("🔄 Restart Level",
                   use_container_width=True):
        st.session_state.new_game = True
        st.session_state.screen   = 'game'
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚙️ Settings",
                 use_container_width=True):
        st.session_state.previous_screen = 'pause'
        st.session_state.screen          = 'settings'
        st.rerun()

    if st.button("🏠 Quit to Home",
                 use_container_width=True):
        st.session_state.screen = 'home'
        st.rerun()

    st.markdown("---")
    st.caption("💡 Tip: Your progress is saved when you resume!")
