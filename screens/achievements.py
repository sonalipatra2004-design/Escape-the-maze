import streamlit as st

ALL_ACHIEVEMENTS = [
    {
        'id':    'first_escape',
        'emoji': '🥇',
        'name':  'First Escape',
        'desc':  'Complete your first level',
        'check': lambda s: s.get('wins', 0) >= 1,
        'reward': 50,
    },
    {
        'id':    'speed_runner',
        'emoji': '⚡',
        'name':  'Speed Runner',
        'desc':  'Finish a level in under 60 seconds',
        'check': lambda s: s.get('fastest_time', 999) < 60,
        'reward': 100,
    },
    {
        'id':    'survivor',
        'emoji': '💀',
        'name':  'Survivor',
        'desc':  'Win a level with only 1 life left',
        'check': lambda s: s.get('won_with_one_life', False),
        'reward': 150,
    },
    {
        'id':    'veteran',
        'emoji': '🎖️',
        'name':  'Veteran',
        'desc':  'Play 10 games',
        'check': lambda s: s.get('games_played', 0) >= 10,
        'reward': 100,
    },
    {
        'id':    'collector',
        'emoji': '💰',
        'name':  'Coin Collector',
        'desc':  'Collect 500 total coins',
        'check': lambda s: s.get('total_coins_earned', 0) >= 500,
        'reward': 200,
    },
    {
        'id':    'explorer',
        'emoji': '🗺️',
        'name':  'Explorer',
        'desc':  'Reach level 5',
        'check': lambda s: s.get('difficulty', 1) >= 5,
        'reward': 200,
    },
    {
        'id':    'powerup_fan',
        'emoji': '⚡',
        'name':  'Power Up Fan',
        'desc':  'Collect 20 power-ups total',
        'check': lambda s: s.get('total_powerups', 0) >= 20,
        'reward': 150,
    },
    {
        'id':    'streak_master',
        'emoji': '🔥',
        'name':  'Streak Master',
        'desc':  'Login 7 days in a row',
        'check': lambda s: s.get('daily_streak', 1) >= 7,
        'reward': 500,
    },
    {
        'id':    'win_streak',
        'emoji': '🏆',
        'name':  'Win Streak',
        'desc':  'Win 5 games in a row',
        'check': lambda s: s.get('win_streak', 0) >= 5,
        'reward': 300,
    },
    {
        'id':    'shopaholic',
        'emoji': '🛒',
        'name':  'Shopaholic',
        'desc':  'Buy 3 items from shop',
        'check': lambda s: s.get('items_bought', 0) >= 3,
        'reward': 100,
    },
]

def check_achievements():
    """Call this after every game to unlock achievements"""
    unlocked = st.session_state.get('unlocked_achievements', [])
    newly_unlocked = []

    for ach in ALL_ACHIEVEMENTS:
        if ach['id'] not in unlocked:
            try:
                if ach['check'](st.session_state):
                    unlocked.append(ach['id'])
                    newly_unlocked.append(ach)
                    # Give reward coins
                    st.session_state.coins = \
                        st.session_state.get('coins', 0) + ach['reward']
            except:
                pass

    st.session_state.unlocked_achievements = unlocked
    return newly_unlocked

def show_achievements():
    st.title("🏅 Achievements")
    st.markdown("---")

    unlocked = st.session_state.get('unlocked_achievements', [])
    total    = len(ALL_ACHIEVEMENTS)
    done     = len(unlocked)

    st.progress(done / total,
                text=f"Unlocked: {done} / {total}")
    st.markdown("---")

    for ach in ALL_ACHIEVEMENTS:
        is_unlocked = ach['id'] in unlocked
        col1, col2 = st.columns([1, 4])

        with col1:
            if is_unlocked:
                st.markdown(f"## {ach['emoji']}")
            else:
                st.markdown("## 🔒")

        with col2:
            if is_unlocked:
                st.markdown(f"**{ach['name']}** ✅")
                st.caption(ach['desc'])
                st.caption(f"Reward earned: 🪙 {ach['reward']} coins")
            else:
                st.markdown(f"**{ach['name']}**")
                st.caption(ach['desc'])
                st.caption(f"Reward: 🪙 {ach['reward']} coins")

        st.markdown("---")

    if st.button("🏠 Back to Home", use_container_width=True):
        st.session_state.screen = 'home'
        st.rerun()
