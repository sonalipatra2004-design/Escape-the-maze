import streamlit as st
import pandas as pd

def show_leaderboard():
    st.title("🏆 Leaderboard")

    tab1, tab2, tab3 = st.tabs(["🌍 Global", "🏳️ Country", "👥 Friends"])

    sample_data = {
        'Rank':   ['🥇 1', '🥈 2', '🥉 3', '4', '5',
                   '6', '7', '8', '9', '10'],
        'Player': ['MazeMaster', 'QuickEscape', 'GhostSlayer',
                   'TrapDodger', 'SpeedRun', 'NightCrawler',
                   'IceBreaker', 'ShadowWalker', 'FireFox',
                   st.session_state.get('username', 'You')],
        'Score':  [9850, 8720, 7650, 6890, 6100,
                   5430, 4890, 4200, 3780,
                   st.session_state.get('score', 0)],
        'Level':  [42, 38, 31, 27, 24, 20, 18, 15, 12,
                   st.session_state.get('difficulty', 1)],
        'Wins':   [210, 185, 156, 134, 118,
                   99,  88,  72,  61,
                   st.session_state.get('wins', 0)],
    }
    df = pd.DataFrame(sample_data)

    with tab1:
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        st.info("🌐 Country ranking coming soon!")

    with tab3:
        st.info("👥 Add friends to compare scores! (Coming Soon)")

    st.markdown("---")
    your_rank = len(sample_data['Player'])
    st.success(f"📍 Your current rank: **#{your_rank}** | "
               f"Score: **{st.session_state.get('score', 0)}**")

    if st.button("🏠 Back to Home"):
        st.session_state.screen = 'home'
        st.rerun()
