import streamlit as st

def show_guide():
    st.title("❓ How To Play")
    st.markdown("---")

    # GOAL
    st.subheader("🎯 Goal")
    st.info(
        "Find the EXIT door 🚪 and escape the maze "
        "before enemies catch you or time runs out!"
    )

    st.markdown("---")

    # CONTROLS
    st.subheader("🕹️ Controls")
    st.markdown("""
    Use the **arrow buttons** on screen to move your player 🧑

    |  Button  | Action        |
    |----------|---------------|
    | ⬆️ Up    | Move Up       |
    | ⬇️ Down  | Move Down     |
    | ⬅️ Left  | Move Left     |
    | ➡️ Right | Move Right    |
    | ⏸️ Pause | Quit to Home  |
    """)

    st.markdown("---")

    # HOW TO WIN
    st.subheader("🏆 How To Win")
    st.success("""
    ✅ Step 1 — Tap PLAY on home screen

    ✅ Step 2 — You are 🧑 (player) in the maze

    ✅ Step 3 — Use arrow buttons to move through paths

    ✅ Step 4 — Avoid walls (you cannot walk through them)

    ✅ Step 5 — Avoid enemies or you lose a life ❤️

    ✅ Step 6 — Collect power-ups on the way ⚡

    ✅ Step 7 — Reach the EXIT door 🚪 to WIN!
    """)

    st.markdown("---")

    # SYMBOLS
    st.subheader("🗺️ What Each Symbol Means")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        | Symbol | Meaning |
        |--------|---------|
        | 🧑 | You (Player) |
        | 🚪 | Exit — reach here to WIN |
        | 👻 | Ghost enemy — smart |
        | 🤖 | Robot enemy — smart |
        | 👹 | Monster — random move |
        | 🕷️ | Spider — fast mover |
        """)

    with col2:
        st.markdown("""
        | Symbol | Meaning |
        |--------|---------|
        | 🗺️ | Map Reveal power-up |
        | ⚡ | Speed Boost power-up |
        | 🛡️ | Shield power-up |
        | ❄️ | Freeze enemies |
        | 💚 | Extra life |
        | 🌀 | Teleport |
        """)

    st.markdown("---")

    # LIVES
    st.subheader("❤️ Lives System")
    st.warning("""
    • You start with **3 lives** ❤️❤️❤️

    • Each time an enemy touches you = lose 1 life

    • Collect 💚 Extra Life power-up to gain lives back

    • 🛡️ Shield blocks ONE enemy hit

    • Lose all 3 lives = Game Over 💀
    """)

    st.markdown("---")

    # POWER UPS
    st.subheader("⚡ Power-ups Guide")
    powerups = [
        ("🗺️ Map Reveal",    "Shows the full maze for 30 seconds"),
        ("⚡ Speed Boost",   "Move faster for 20 seconds"),
        ("🛡️ Shield",        "Blocks one enemy hit automatically"),
        ("❄️ Freeze",        "Freezes ALL enemies for 15 seconds"),
        ("💚 Extra Life",    "Adds +1 life instantly"),
        ("🌀 Teleport",      "Jumps you to a random safe spot"),
        ("🪙 Double Coins",  "Earn 2x coins for 60 seconds"),
        ("🔍 Trap Detector", "Shows all hidden traps for 25 seconds"),
    ]
    for emoji_name, desc in powerups:
        st.markdown(f"**{emoji_name}** — {desc}")

    st.markdown("---")

    # SCORING
    st.subheader("🪙 Coins & Scoring")
    st.info("""
    • Reach exit faster = more coins earned 🪙

    • Fewer moves = higher score

    • Coins are used in the 🛒 Shop

    • Buy characters, power-ups and themes with coins
    """)

    st.markdown("---")

    # TIPS
    st.subheader("💡 Beginner Tips")
    st.markdown("""
    1. **Always look ahead** — plan your path before moving
    2. **Collect power-ups first** — they help a lot
    3. **Freeze enemies** ❄️ when surrounded
    4. **Use shield** 🛡️ before entering risky areas
    5. **Follow the open paths** — walls are dark colored
    6. **Exit 🚪 is always** in the bottom right area
    7. **Lower difficulty first** — practice in Settings ⚙️
    """)

    st.markdown("---")

    # DIFFICULTY
    st.subheader("⚙️ Difficulty Levels")
    diff_data = {
        "Level": ["1 — Easy", "2 — Normal", "3 — Hard",
                  "4 — Expert", "5 — Insane"],
        "Maze Size": ["Small", "Medium", "Large", "Huge", "Massive"],
        "Enemies": ["2", "3", "4", "5", "6+"],
        "Enemy AI": ["Dumb", "Slow", "Smart", "Fast", "Very Fast"],
    }
    import pandas as pd
    st.dataframe(pd.DataFrame(diff_data),
                 use_container_width=True, hide_index=True)

    st.markdown("---")

    col1, col2 = st.columns(2)
    if col1.button("▶️ Play Now!", use_container_width=True, type="primary"):
        st.session_state.screen = 'game'
        st.session_state.new_game = True
        st.rerun()
    if col2.button("🏠 Back to Home", use_container_width=True):
        st.session_state.screen = 'home'
        st.rerun()
