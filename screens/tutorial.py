import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

TUTORIAL_STEPS = [
    {
        'title':   '👋 Welcome to AI Maze!',
        'message': 'This is YOU → 🧑 You are inside a maze. Your job is to find the EXIT door 🚪',
        'tip':     'You are always placed at the TOP LEFT of the maze',
    },
    {
        'title':   '🕹️ How to Move',
        'message': 'Use the arrow buttons below the maze to move UP, DOWN, LEFT, RIGHT',
        'tip':     'You CANNOT walk through walls. Only move through open white paths!',
    },
    {
        'title':   '🚪 Find the Exit',
        'message': 'The EXIT door 🚪 is always at the BOTTOM RIGHT of the maze. Reach it to WIN!',
        'tip':     'Plan your path — look ahead before moving!',
    },
    {
        'title':   '👻 Watch Out for Enemies',
        'message': 'Enemies like 👻 Ghost and 🤖 Robot will chase you. If they touch you, you lose a life ❤️',
        'tip':     'Use ❄️ Freeze power-up to stop enemies!',
    },
    {
        'title':   '⚡ Collect Power-ups',
        'message': 'You will see special items on the maze floor. Walk over them to collect automatically!',
        'tip':     '🛡️ Shield blocks one hit. 💚 Extra Life gives you +1 life!',
    },
    {
        'title':   '🎉 You are Ready!',
        'message': 'You know everything you need to play! Start with Easy difficulty and work your way up.',
        'tip':     'Visit ❓ How To Play anytime for more tips!',
    },
]

def draw_tutorial_maze():
    """Draw a simple small demo maze"""
    maze = np.array([
        [1,1,1,1,1,1,1],
        [0,0,0,1,0,0,1],
        [1,1,0,1,0,1,1],
        [1,1,0,0,0,1,1],
        [1,1,1,1,0,1,1],
        [1,1,1,1,0,0,0],
        [1,1,1,1,1,1,1],
    ])

    fig, ax = plt.subplots(figsize=(4, 4))
    fig.patch.set_facecolor('#f0f0f0')
    ax.set_facecolor('#f0f0f0')

    rows, cols = maze.shape
    for r in range(rows):
        for c in range(cols):
            color = '#333333' if maze[r][c] == 1 else '#ffffff'
            rect = patches.Rectangle(
                (c, rows-r-1), 1, 1,
                facecolor=color, edgecolor='#cccccc')
            ax.add_patch(rect)

    # Player at start
    ax.text(0.5, rows-1-0.5, '🧑',
            ha='center', va='center', fontsize=14)
    # Exit
    ax.text(6.5, 0.5, '🚪',
            ha='center', va='center', fontsize=14)
    # Enemy
    ax.text(4.5, rows-1-0.5, '👻',
            ha='center', va='center', fontsize=12)
    # Power-up
    ax.text(2.5, rows-3-0.5, '⚡',
            ha='center', va='center', fontsize=11)

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.axis('off')
    plt.tight_layout(pad=0)
    return fig

def show_tutorial():
    st.title("📖 Tutorial")

    step = st.session_state.get('tutorial_step', 0)
    total_steps = len(TUTORIAL_STEPS)

    # Progress
    st.progress((step + 1) / total_steps,
                text=f"Step {step+1} of {total_steps}")
    st.markdown("---")

    # Current step
    current = TUTORIAL_STEPS[step]
    st.subheader(current['title'])
    st.info(current['message'])
    st.success(f"💡 Tip: {current['tip']}")

    # Show demo maze
    st.markdown("**Demo Maze:**")
    st.pyplot(draw_tutorial_maze(),
              use_container_width=True)

    st.markdown("---")

    # Navigation
    col1, col2, col3 = st.columns(3)

    if step > 0:
        if col1.button("⬅️ Back",
                       use_container_width=True):
            st.session_state.tutorial_step = step - 1
            st.rerun()

    if step < total_steps - 1:
        if col3.button("Next ➡️",
                       use_container_width=True,
                       type="primary"):
            st.session_state.tutorial_step = step + 1
            st.rerun()
    else:
        if col3.button("▶️ Play Now!",
                       use_container_width=True,
                       type="primary"):
            st.session_state.tutorial_step = 0
            st.session_state.screen        = 'game'
            st.session_state.new_game      = True
            st.rerun()

    if col2.button("🏠 Home",
                   use_container_width=True):
        st.session_state.tutorial_step = 0
        st.session_state.screen        = 'home'
        st.rerun()
