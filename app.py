import streamlit as st

st.set_page_config(
    page_title="AI Maze Game",
    page_icon="🌀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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
from screens.home         import show_home
from screens.profile      import show_profile
from screens.shop         import show_shop
from screens.leaderboard  import show_leaderboard
from screens.settings     import show_settings
from screens.game_screen  import show_game, show_win, show_game_over
from screens.guide        import show_guide
from screens.daily_reward import show_daily_reward
from screens.achievements import show_achievements, check_achievements
from screens.statistics   import show_statistics
from screens.missions     import show_missions
from screens.tutorial     import show_tutorial
from screens.pause        import show_pause

# Default session state values
defaults = {
    'screen':              'home',
    'coins':               100,
    'gems':                10,
    'difficulty':          1,
    'theme':               'Space',
    'new_game':            True,
    'username':            'MazeRunner',
    'player_level':        1,
    'xp':                  0,
    'total_xp':            0,
    'games_played':        0,
    'wins':                0,
    'score':               0,
    'best_time':           '--',
    'badges':              ['🌟 First Visit'],
    'avatar_idx':          0,
    'dark_mode':           False,
    'maze_size':           'Medium',
    'colorblind':          False,
    'large_ui':            False,
    'message':             '',
    'daily_streak':        1,
    'last_reward_date':    '',
    'unlocked_achievements': [],
    'total_coins_earned':  0,
    'total_gems_earned':   0,
    'fastest_time':        0,
    'total_time_played':   0,
    'avg_moves':           0,
    'game_history':        [],
    'win_streak':          0,
    'best_win_streak':     0,
    'total_powerups':      0,
    'items_bought':        0,
    'favourite_powerup':   'None',
    'tutorial_step':       0,
    'games_played_today':  0,
    'wins_today':          0,
    'powerups_today':      0,
    'claimed_missions':    [],
    'missions_date':       '',
    'won_with_one_life':   False,
    'hints_used':          0,
    'current_hint':        '',
    'show_hint':           False,
    'xp_earned_last':      0,
    'level_up_message':    '',
    'manual_theme':        None,
    'wins_week':           0,
    'games_played_week':   0,
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Screen router
screen = st.session_state.screen

if   screen == 'home':         show_home()
elif screen == 'game':         show_game()
elif screen == 'win':          show_win()
elif screen == 'game_over':    show_game_over()
elif screen == 'profile':      show_profile()
elif screen == 'shop':         show_shop()
elif screen == 'leaderboard':  show_leaderboard()
elif screen == 'settings':     show_settings()
elif screen == 'guide':        show_guide()
elif screen == 'daily_reward': show_daily_reward()
elif screen == 'achievements': show_achievements()
elif screen == 'statistics':   show_statistics()
elif screen == 'missions':     show_missions()
elif screen == 'tutorial':     show_tutorial()
elif screen == 'pause':        show_pause()
else:
    st.error(f"Screen not found: {screen}")
    if st.button("🏠 Go Home"):
        st.session_state.screen = 'home'
        st.rerun()
