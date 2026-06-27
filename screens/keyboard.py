import streamlit as st

KEYBOARD_JS = """
<script>
// Keyboard controls for maze
document.addEventListener('keydown', function(e) {
    let btn = null;

    if (e.key === 'ArrowUp'    || e.key === 'w' || e.key === 'W') {
        btn = document.querySelector('[data-testid="baseButton-secondary"]:nth-of-type(1)');
        e.preventDefault();
    }
    if (e.key === 'ArrowDown'  || e.key === 's' || e.key === 'S') {
        btn = document.querySelector('[data-testid="baseButton-secondary"]:nth-of-type(4)');
        e.preventDefault();
    }
    if (e.key === 'ArrowLeft'  || e.key === 'a' || e.key === 'A') {
        btn = document.querySelector('[data-testid="baseButton-secondary"]:nth-of-type(2)');
        e.preventDefault();
    }
    if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') {
        btn = document.querySelector('[data-testid="baseButton-secondary"]:nth-of-type(3)');
        e.preventDefault();
    }
    if (e.key === 'Escape' || e.key === 'p' || e.key === 'P') {
        btn = document.querySelector('[data-testid="baseButton-secondary"]:nth-of-type(5)');
        e.preventDefault();
    }

    if (btn) btn.click();
});
</script>
"""

def inject_keyboard_controls():
    """Call this inside show_game() to enable keyboard"""
    st.components.v1.html(KEYBOARD_JS, height=0)

def show_keyboard_help():
    """Small keyboard guide shown during game"""
    with st.expander("⌨️ Keyboard Shortcuts"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            | Key | Action |
            |-----|--------|
            | ⬆️ Arrow / W | Move Up |
            | ⬇️ Arrow / S | Move Down |
            | ⬅️ Arrow / A | Move Left |
            | ➡️ Arrow / D | Move Right |
            | P / Esc | Pause |
            """)
        with col2:
            st.info("💡 Use keyboard for faster gameplay on desktop!")
