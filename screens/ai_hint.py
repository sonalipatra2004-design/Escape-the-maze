import streamlit as st
import numpy as np
from collections import deque

def find_shortest_path(maze, start, end):
    """BFS to find shortest path"""
    queue   = deque([(start, [start])])
    visited = {start}

    while queue:
        (r, c), path = queue.popleft()
        if (r, c) == end:
            return path
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if (0 <= nr < maze.shape[0] and
                0 <= nc < maze.shape[1] and
                maze[nr][nc] == 0 and
                (nr, nc) not in visited):
                visited.add((nr, nc))
                queue.append(((nr,nc), path+[(nr,nc)]))
    return []

def get_next_move_direction(current_pos, next_pos):
    """Convert position difference to direction"""
    dr = next_pos[0] - current_pos[0]
    dc = next_pos[1] - current_pos[1]

    if dr == -1: return "⬆️ Move UP"
    if dr ==  1: return "⬇️ Move DOWN"
    if dc == -1: return "⬅️ Move LEFT"
    if dc ==  1: return "➡️ Move RIGHT"
    return "🚪 You are at the exit!"

def get_ai_hint():
    """Get AI pathfinding hint"""
    maze     = st.session_state.get('maze', None)
    player   = st.session_state.get('player', None)
    exit_pos = st.session_state.get('exit_pos', None)

    if maze is None or player is None or exit_pos is None:
        return "Start a game first!", "❓", 0

    start = player.get_position()
    end   = exit_pos

    path = find_shortest_path(maze, start, end)

    if not path:
        return "No path found! Try a different route.", "🤔", 0

    if len(path) <= 1:
        return "🎉 You are at the exit! Go through the door!", "🚪", 0

    next_step     = path[1]
    direction     = get_next_move_direction(start, next_step)
    steps_left    = len(path) - 1

    # Smart tip based on situation
    enemies  = st.session_state.get('enemies', [])
    near_enemy = any(
        abs(e.row - start[0]) <= 2 and
        abs(e.col - start[1]) <= 2
        for e in enemies
    )

    if near_enemy:
        tip = (f"⚠️ Enemy nearby! {direction} "
               f"({steps_left} steps to exit)")
    elif steps_left <= 3:
        tip = (f"🏃 Almost there! {direction} "
               f"({steps_left} steps to exit!)")
    elif steps_left <= 10:
        tip = (f"✅ Good progress! {direction} "
               f"({steps_left} steps to exit)")
    else:
        tip = (f"🗺️ {direction} "
               f"({steps_left} steps to exit)")

    return tip, direction, steps_left

def show_hint_button():
    """Show hint button during game"""
    hints_used = st.session_state.get('hints_used', 0)
    max_hints  = 3 + st.session_state.get('difficulty', 1)

    col1, col2 = st.columns([1, 3])
    with col1:
        st.caption(f"Hints: {hints_used}/{max_hints}")

    with col2:
        if hints_used < max_hints:
            if st.button("💡 Get Hint",
                         use_container_width=True):
                hint, direction, steps = get_ai_hint()
                st.session_state.current_hint  = hint
                st.session_state.hints_used    = hints_used + 1
                st.session_state.show_hint     = True
                st.rerun()
        else:
            st.warning("No hints left this level!")

    # Show hint if active
    if st.session_state.get('show_hint', False):
        hint = st.session_state.get('current_hint', '')
        st.info(f"💡 AI Hint: {hint}")
        if st.button("✖️ Hide Hint"):
            st.session_state.show_hint = False
            st.rerun()
