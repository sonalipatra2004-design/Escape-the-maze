import streamlit as st

st.set_page_config(
    page_title="AI Maze Game",
    page_icon="🌀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Global dark theme CSS
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0a1e 0%, #1a0a2e 50%, #0a1a2e 100%);
    color: white;
}
[data-testid="stHeader"]    { background: transparent; }
[data-testid="stSidebar"]   { background: #0a0a2e; }
.stButton > button {
    background: linear-gradient(135deg, #1e3a5f, #2d5a8f);
    color: white !important;
    border: 1px solid #4a90d9;
    border-radius: 10px;
    font-weight: bold;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2d5a8f, #4a90d9);
    box-shadow: 0 0 15px #4a90d9;
    transform: scale(1.02);
}
.stMetric { color: white; }
</style>
""", unsafe_allow_html=True)

# Import all screens
from screens.home        import show_home
from screens.profile     import show_profile
from screens.shop        import show_shop
from screens.leaderboard import show_leaderboard
from screens.settings    import show_settings
from screens.game_screen import show_game, show_win, show_game_over

# Default session state values
defaults = {
    'screen':       'home',
    'coins':        100,
    'gems':         10,
    'difficulty':   1,
    'theme':        'Space',
    'new_game':     True,
    'username':     'MazeRunner',
    'player_level': 1,
    'xp':           0,
    'games_played': 0,
    'wins':         0,
    'score':        0,
    'best_time':    '--',
    'badges':       ['🌟 First Visit'],
    'avatar_idx':   0,
    'dark_mode':    True,
    'maze_size':    'Medium',
    'colorblind':   False,
    'large_ui':     False,
    'message':      '',
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Screen router
screen = st.session_state.screen

if   screen == 'home':        show_home()
elif screen == 'game':        show_game()
elif screen == 'win':         show_win()
elif screen == 'game_over':   show_game_over()
elif screen == 'profile':     show_profile()
elif screen == 'shop':        show_shop()
elif screen == 'leaderboard': show_leaderboard()
elif screen == 'settings':    show_settings()
else:
    st.error(f"Screen not found: {screen}")
    if st.button("🏠 Go Home"):
        st.session_state.screen = 'home'
        st.rerun()
