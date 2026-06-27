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
    background: #ffffff;
    color: #000000;
}
[data-testid="stHeader"] { background: #ffffff; }
p, span, label, div, h1, h2, h3, h4, h5, h6 {
    color: #000000 !important;
}
[data-testid="stMetricLabel"] { color: #0066cc !important; }
[data-testid="stMetricValue"] { color: #000000 !important; }
.stRadio label { color: #000000 !important; }
.stSelectbox label { color: #000000 !important; }
.stSelectbox div { color: #000000 !important; }
.stSlider label { color: #000000 !important; }
.stTabs [data-baseweb="tab"] {
    color: #000000 !important;
    background: #f0f0f0;
}
.stTabs [aria-selected="true"] {
    color: #0066cc !important;
    border-bottom: 2px solid #0066cc;
}
.stTextInput input {
    background: #f0f0f0;
    color: #000000 !important;
    border: 1px solid #0066cc;
    border-radius: 8px;
}
.stAlert { color: #000000 !important; }
.stCaption { color: #555555 !important; }
.stButton > button {
    background: #0066cc;
    color: #ffffff !important;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    background: #0044aa;
    box-shadow: 0 0 10px #0066cc;
    transform: scale(1.02);
}
[data-testid="stSidebar"] {
    background: #f5f5f5;
    color: #000000;
}
</style>
""", unsafe_allow_html=True)

# Import all screens
from screens.home        import show_home
from screens.profile     import show_profile
from screens.shop        import show_shop
from screens.leaderboard import show_leaderboard
from screens.settings    import show_settings
from screens.guide       import show_guide
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
elif screen == from screens.guide       import show_guide'shop':        show_shop()
elif screen == 'leaderboard': show_leaderboard()
elif screen == 'settings':    show_settings()
elif screen == 'guide':       show_guide()
else:
    st.error(f"Screen not found: {screen}")
    if st.button("🏠 Go Home"):
        st.session_state.screen = 'home'
        st.rerun()
