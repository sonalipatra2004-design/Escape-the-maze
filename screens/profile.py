import streamlit as st

def get_level_title(level):
    LEVEL_TITLES = [
        'Newbie', 'Beginner', 'Explorer', 'Adventurer',
        'Maze Walker', 'Maze Runner', 'Maze Hunter',
        'Maze Master', 'Shadow Runner', 'Ghost Chaser',
        'Speed Demon', 'Trap Dodger', 'Elite Runner',
        'Maze Legend', 'Grand Master', 'Maze God',
        'Immortal', 'Phantom', 'Titan', 'Champion',
        'AI Maze King',
    ]
    idx = min(level - 1, len(LEVEL_TITLES) - 1)
    return LEVEL_TITLES[idx]

def show_xp_bar():
    LEVEL_THRESHOLDS = [
        0, 100, 250, 450, 700, 1000,
        1350, 1750, 2200, 2700, 3250,
        3850, 4500, 5200, 5950, 6750,
        7600, 8500, 9450, 10450, 11500,
    ]
    total_xp = st.session_state.get('total_xp', 0)
    level    = st.session_state.get('player_level', 1)

    current_threshold = LEVEL_THRESHOLDS[
        min(level - 1, len(LEVEL_THRESHOLDS) - 1)]
    next_idx = min(level, len(LEVEL_THRESHOLDS) - 1)
    next_threshold = LEVEL_THRESHOLDS[next_idx]

    xp_in_level = total_xp - current_threshold
    xp_needed   = max(next_threshold - current_threshold, 1)
    progress    = min(xp_in_level / xp_needed, 1.0)

    st.progress(progress,
                text=f"XP: {xp_in_level}/{xp_needed} to next level")

def show_profile():
    st.title("👤 Profile")

    col1, col2 = st.columns([1, 2])
    with col1:
        avatars = ['🧙', '🧝', '🤖', '👸', '🦸', '🧜']
        idx     = st.session_state.get('avatar_idx', 0)
        chosen  = st.radio("Choose Avatar", avatars,
                           index=idx, horizontal=True)
        st.session_state.avatar_idx = avatars.index(chosen)
        st.markdown(
            f"<h1 style='text-align:center'>{chosen}</h1>",
            unsafe_allow_html=True)

    with col2:
        username = st.text_input(
            "Username",
            value=st.session_state.get('username', 'MazeRunner'))
        st.session_state.username = username

        level = st.session_state.get('player_level', 1)
        title = get_level_title(level)
        st.write(f"**Level {level}** — {title}")
        show_xp_bar()

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
    c1.metric("Games Played",
              st.session_state.get('games_played', 0))
    c2.metric("Wins",
              st.session_state.get('wins', 0))
    fastest = st.session_state.get('fastest_time', 0)
    if fastest > 0:
        mins = fastest // 60
        secs = fastest % 60
        best = f"{mins:02d}:{secs:02d}"
    else:
        best = '--'
    c3.metric("Best Time", best)

    st.markdown("---")
    st.subheader("🏆 Achievements")
    unlocked = st.session_state.get('unlocked_achievements', [])
    st.write(f"Unlocked: **{len(unlocked)}** achievements")
    if st.button("View All Achievements",
                 use_container_width=True):
        st.session_state.screen = 'achievements'
        st.rerun()

    st.markdown("---")
    if st.button("🏠 Back to Home",
                 use_container_width=True):
        st.session_state.screen = 'home'
        st.rerun()
