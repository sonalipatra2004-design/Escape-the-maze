import streamlit as st
import pandas as pd

def show_statistics():
    st.title("📊 Statistics")
    st.markdown("---")

    # Main stats
    st.subheader("🎮 Game Stats")
    c1, c2, c3 = st.columns(3)
    c1.metric("Games Played",
              st.session_state.get('games_played', 0))
    c2.metric("Total Wins",
              st.session_state.get('wins', 0))
    games = st.session_state.get('games_played', 0)
    wins  = st.session_state.get('wins', 0)
    rate  = f"{int((wins/games)*100)}%" if games > 0 else "0%"
    c3.metric("Win Rate", rate)

    st.markdown("---")

    # Time stats
    st.subheader("⏱️ Time Stats")
    c1, c2, c3 = st.columns(3)
    fastest = st.session_state.get('fastest_time', 0)
    mins    = fastest // 60
    secs    = fastest % 60
    c1.metric("Fastest Escape",
              f"{mins:02d}:{secs:02d}" if fastest > 0 else "--")
    total_time = st.session_state.get('total_time_played', 0)
    tmins = total_time // 60
    c2.metric("Total Time Played", f"{tmins} mins")
    avg_moves = st.session_state.get('avg_moves', 0)
    c3.metric("Avg Moves Per Game", avg_moves)

    st.markdown("---")

    # Economy stats
    st.subheader("💰 Economy Stats")
    c1, c2, c3 = st.columns(3)
    c1.metric("🪙 Total Coins Earned",
              st.session_state.get('total_coins_earned', 0))
    c2.metric("💎 Total Gems Earned",
              st.session_state.get('total_gems_earned', 0))
    c3.metric("🛒 Items Bought",
              st.session_state.get('items_bought', 0))

    st.markdown("---")

    # Power-up stats
    st.subheader("⚡ Power-up Stats")
    c1, c2 = st.columns(2)
    c1.metric("Total Power-ups Collected",
              st.session_state.get('total_powerups', 0))
    fav = st.session_state.get('favourite_powerup', 'None')
    c2.metric("Favourite Power-up", fav)

    st.markdown("---")

    # Level stats
    st.subheader("🎯 Level Stats")
    c1, c2, c3 = st.columns(3)
    c1.metric("Highest Level Reached",
              st.session_state.get('difficulty', 1))
    c2.metric("Current Win Streak",
              st.session_state.get('win_streak', 0))
    c3.metric("Best Win Streak",
              st.session_state.get('best_win_streak', 0))

    st.markdown("---")

    # Recent games table
    st.subheader("📋 Recent Games")
    history = st.session_state.get('game_history', [])

    if history:
        df = pd.DataFrame(history)
        st.dataframe(df, use_container_width=True,
                     hide_index=True)
    else:
        st.info("No games played yet! Play your first game to see stats here.")

    st.markdown("---")

    col1, col2 = st.columns(2)
    if col1.button("▶️ Play Now",
                   use_container_width=True, type="primary"):
        st.session_state.screen  = 'game'
        st.session_state.new_game = True
        st.rerun()
    if col2.button("🏠 Back to Home",
                   use_container_width=True):
        st.session_state.screen = 'home'
        st.rerun()
