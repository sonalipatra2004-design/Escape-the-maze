import streamlit as st
from datetime import datetime, date

def check_daily_reward():
    today = str(date.today())
    last_claim = st.session_state.get('last_reward_date', '')
    return today != last_claim

def show_daily_reward():
    st.title("🎁 Daily Reward")
    st.markdown("---")

    # Reward schedule
    rewards = [
        (1,  "🪙 50 Coins",          {'coins': 50}),
        (2,  "🪙 100 Coins",         {'coins': 100}),
        (3,  "💎 1 Gem",             {'gems': 1}),
        (4,  "🪙 150 Coins",         {'coins': 150}),
        (5,  "💎 2 Gems",            {'gems': 2}),
        (6,  "🪙 200 Coins",         {'coins': 200}),
        (7,  "🪙 500 Coins + 💎 5",  {'coins': 500, 'gems': 5}),
    ]

    streak = st.session_state.get('daily_streak', 1)
    streak = max(1, min(streak, 7))

    st.subheader(f"🔥 Current Streak: Day {streak}")
    st.progress(streak / 7, text=f"Day {streak} of 7")
    st.markdown("---")

    # Show all 7 days
    st.subheader("📅 Weekly Rewards")
    cols = st.columns(7)
    for i, (day, reward, _) in enumerate(rewards):
        with cols[i]:
            if day < streak:
                st.markdown(f"✅\n**Day {day}**\n{reward}")
            elif day == streak:
                st.markdown(f"🎁\n**Day {day}**\n{reward}")
            else:
                st.markdown(f"🔒\n**Day {day}**\n{reward}")

    st.markdown("---")

    # Claim button
    today = str(date.today())
    last_claim = st.session_state.get('last_reward_date', '')
    already_claimed = today == last_claim

    if already_claimed:
        st.success("✅ You already claimed today's reward! Come back tomorrow.")
        next_reward_day = min(streak + 1, 7)
        st.info(f"🎁 Tomorrow's reward: **{rewards[next_reward_day-1][1]}**")
    else:
        day_reward = rewards[streak - 1]
        st.info(f"🎁 Today's reward: **{day_reward[1]}**")

        if st.button("🎁 CLAIM REWARD!", type="primary",
                     use_container_width=True):
            # Give reward
            reward_items = day_reward[2]
            if 'coins' in reward_items:
                st.session_state.coins = \
                    st.session_state.get('coins', 0) + reward_items['coins']
            if 'gems' in reward_items:
                st.session_state.gems = \
                    st.session_state.get('gems', 0) + reward_items['gems']

            # Update streak
            st.session_state.last_reward_date = today
            st.session_state.daily_streak = \
                (streak % 7) + 1

            st.balloons()
            st.success(f"🎉 Claimed: {day_reward[1]}!")
            st.rerun()

    st.markdown("---")
    if st.button("🏠 Back to Home", use_container_width=True):
        st.session_state.screen = 'home'
        st.rerun()
