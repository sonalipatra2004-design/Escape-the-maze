import streamlit as st

def show_profile():
    st.title("👤 Profile")

    col1, col2 = st.columns([1, 2])
    with col1:
        avatars = ['🧙', '🧝', '🤖', '👸', '🦸', '🧜']
        idx = st.session_state.get('avatar_idx', 0)
        chosen = st.radio("Choose Avatar", avatars,
                          index=idx, horizontal=True)
        st.session_state.avatar_idx = avatars.index(chosen)
        st.markdown(f"<h1 style='text-align:center'>{chosen}</h1>",
                    unsafe_allow_html=True)

    with col2:
        username = st.text_input("Username",
                    value=st.session_state.get('username', 'MazeRunner'))
        st.session_state.username = username

        level = st.session_state.get('player_level', 1)
        xp    = st.session_state.get('xp', 0)
        st.write(f"**Level:** {level}")
        st.progress(min(xp / 100, 1.0), text=f"XP: {xp} / 100")

        c1, c2 = st.columns(2)
        c1.metric("🪙 Coins", st.session_state.get('coins', 0))
        c2.metric("💎 Gems",  st.session_state.get('gems', 0))

    st.markdown("---")
    st.subheader("🏅 Badges")
    badges = st.session_state.get('badges', ['🌟 First Visit'])
    st.write("   ".join(badges))

    st.markdown("---")
    st.subheader("📊 Stats")
    c1, c2, c3 = st.columns(3)
    c1.metric("Games Played", st.session_state.get('games_played', 0))
    c2.metric("Wins",         st.session_state.get('wins', 0))
    c3.metric("Best Time",    st.session_state.get('best_time', '--'))

    st.markdown("---")
    if st.button("🏠 Back to Home"):
        st.session_state.screen = 'home'
        st.rerun()
