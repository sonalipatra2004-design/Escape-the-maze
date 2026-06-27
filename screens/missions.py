import streamlit as st
from datetime import date

DAILY_MISSIONS = [
    {
        'id':     'play_3_games',
        'name':   'Play 3 Games Today',
        'emoji':  '🎮',
        'target': 3,
        'key':    'games_played_today',
        'reward': {'coins': 50},
        'reward_text': '🪙 50 Coins',
    },
    {
        'id':     'win_2_games',
        'name':   'Win 2 Games Today',
        'emoji':  '🏆',
        'target': 2,
        'key':    'wins_today',
        'reward': {'coins': 100},
        'reward_text': '🪙 100 Coins',
    },
    {
        'id':     'collect_5_powerups',
        'name':   'Collect 5 Power-ups',
        'emoji':  '⚡',
        'target': 5,
        'key':    'powerups_today',
        'reward': {'coins': 30},
        'reward_text': '🪙 30 Coins',
    },
]

WEEKLY_MISSIONS = [
    {
        'id':     'play_10_games_week',
        'name':   'Play 10 Games This Week',
        'emoji':  '🎮',
        'target': 10,
        'key':    'games_played_week',
        'reward': {'coins': 200},
        'reward_text': '🪙 200 Coins',
    },
    {
        'id':     'win_5_games_week',
        'name':   'Win 5 Games This Week',
        'emoji':  '🏆',
        'target': 5,
        'key':    'wins_week',
        'reward': {'gems': 2},
        'reward_text': '💎 2 Gems',
    },
    {
        'id':     'reach_level_5',
        'name':   'Reach Level 5',
        'emoji':  '⬆️',
        'target': 5,
        'key':    'difficulty',
        'reward': {'gems': 3},
        'reward_text': '💎 3 Gems',
    },
]

def reset_daily_missions():
    today = str(date.today())
    if st.session_state.get('missions_date', '') != today:
        st.session_state.missions_date    = today
        st.session_state.games_played_today = 0
        st.session_state.wins_today         = 0
        st.session_state.powerups_today     = 0
        st.session_state.claimed_missions   = []

def show_missions():
    st.title("🎯 Missions")
    reset_daily_missions()
    st.markdown("---")

    tab1, tab2 = st.tabs(["📅 Daily", "📆 Weekly"])

    def render_missions(missions_list):
        claimed = st.session_state.get('claimed_missions', [])
        for m in missions_list:
            current = st.session_state.get(m['key'], 0)
            target  = m['target']
            progress = min(current / target, 1.0)
            done     = progress >= 1.0
            claimed_ = m['id'] in claimed

            col1, col2 = st.columns([3, 1])
            with col1:
                status = "✅" if done else "🔄"
                st.markdown(
                    f"{m['emoji']} **{m['name']}** {status}")
                st.progress(progress,
                    text=f"{min(current, target)}/{target}")
                st.caption(f"Reward: {m['reward_text']}")

            with col2:
                if done and not claimed_:
                    if st.button("Claim!",
                                 key=f"claim_{m['id']}",
                                 type="primary"):
                        r = m['reward']
                        if 'coins' in r:
                            st.session_state.coins = \
                                st.session_state.get('coins',0) + r['coins']
                        if 'gems' in r:
                            st.session_state.gems = \
                                st.session_state.get('gems',0) + r['gems']
                        claimed.append(m['id'])
                        st.session_state.claimed_missions = claimed
                        st.success("Claimed!")
                        st.rerun()
                elif claimed_:
                    st.success("✅ Done")
                else:
                    st.info("🔒")

            st.markdown("---")

    with tab1:
        st.subheader("📅 Daily Missions")
        st.caption("Resets every day at midnight")
        render_missions(DAILY_MISSIONS)

    with tab2:
        st.subheader("📆 Weekly Missions")
        st.caption("Resets every Monday")
        render_missions(WEEKLY_MISSIONS)

    if st.button("🏠 Back to Home", use_container_width=True):
        st.session_state.screen = 'home'
        st.rerun()
