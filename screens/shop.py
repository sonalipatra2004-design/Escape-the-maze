import streamlit as st

def show_shop():
    st.title("🛒 Shop")

    coins = st.session_state.get('coins', 0)
    st.metric("🪙 Your Coins", coins)
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["🎭 Characters", "⚡ Power-ups", "🎨 Themes"])

    with tab1:
        items = [
            ('🧙 Wizard',   100, 'Bonus hint every 3 levels'),
            ('🤖 Android',  150, 'Auto-detects traps nearby'),
            ('🦸 Hero',     200, 'Extra shield per level'),
            ('👸 Princess', 120, 'Earns double coins'),
            ('🧜 Mermaid',  180, 'Passes through water tiles'),
            ('🧝 Elf',      130, 'Faster movement speed'),
        ]
        for name, price, desc in items:
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.write(f"**{name}** — {desc}")
            col2.write(f"🪙 {price}")
            if col3.button("Buy", key=f"char_{name}"):
                if st.session_state.get('coins', 0) >= price:
                    st.session_state.coins -= price
                    st.success(f"✅ {name} unlocked!")
                else:
                    st.error("❌ Not enough coins!")

    with tab2:
        powerups = [
            ('🗺️ Map Reveal',   50, 'See full maze 30s'),
            ('⚡ Speed Boost',   30, 'Move 2x for 20s'),
            ('🛡️ Shield',       40, 'Block one hit'),
            ('❄️ Freeze',       60, 'Stop enemies 15s'),
            ('💚 Extra Life',    80, '+1 life'),
            ('🌀 Teleport',      70, 'Jump to random cell'),
            ('🪙 Double Coins',  45, '2x coins for 60s'),
            ('🔍 Trap Detector', 55, 'Show all traps 25s'),
        ]
        for name, price, desc in powerups:
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.write(f"**{name}** — {desc}")
            col2.write(f"🪙 {price}")
            if col3.button("Buy", key=f"pu_{name}"):
                if st.session_state.get('coins', 0) >= price:
                    st.session_state.coins -= price
                    st.success(f"✅ {name} added!")
                else:
                    st.error("❌ Not enough coins!")

    with tab3:
        themes = [
            ('🌲 Forest',  'Green walls, nature paths',  0),
            ('🏜️ Desert',  'Sandy walls, golden paths',  80),
            ('❄️ Ice',     'Blue walls, white paths',    100),
            ('🌋 Lava',    'Red walls, orange paths',    120),
            ('🚀 Space',   'Dark walls, grey paths',     0),
            ('👻 Haunted', 'Purple walls, eerie paths',  150),
        ]
        for name, desc, price in themes:
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.write(f"**{name}** — {desc}")
            col2.write(f"{'Free' if price == 0 else f'🪙 {price}'}")
            theme_key = name.split()[1]
            if col3.button("Select", key=f"theme_{name}"):
                if price == 0 or st.session_state.get('coins', 0) >= price:
                    if price > 0:
                        st.session_state.coins -= price
                    st.session_state.theme = theme_key
                    st.success(f"✅ {name} theme selected!")
                else:
                    st.error("❌ Not enough coins!")

    st.markdown("---")
    if st.button("🏠 Back to Home"):
        st.session_state.screen = 'home'
        st.rerun()
