import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time
from game.maze_generator import MazeGenerator
from game.player import Player
from game.enemies import Enemy

THEME_COLORS = {
    'Forest':  {'wall': '#2d5a1b', 'path': '#90EE90', 'bg': '#1a3a0a'},
    'Desert':  {'wall': '#8B6914', 'path': '#F4D03F', 'bg': '#5D4037'},
    'Ice':     {'wall': '#4FC3F7', 'path': '#E3F2FD', 'bg': '#0D47A1'},
    'Lava':    {'wall': '#BF360C', 'path': '#FF8F00', 'bg': '#3E2723'},
    'Space':   {'wall': '#37474F', 'path': '#B0BEC5', 'bg': '#0A0A2E'},
    'Haunted': {'wall': '#4A0080', 'path': '#CE93D8', 'bg': '#1A0030'},
}

def init_game():
    difficulty = st.session_state.get('difficulty', 1)
    theme      = st.session_state.get('theme', 'Space')
    size       = 13 + (difficulty * 2)

    gen    = MazeGenerator(size, size)
    maze   = gen.generate(difficulty)
    player = Player(gen.get_start_position())

    enemies_pos = gen.place_enemies(count=difficulty + 1)
    enemy_types = ['ghost', 'robot', 'monster', 'spider']
    enemies = [
        Enemy(pos, enemy_types[i % len(enemy_types)])
        for i, pos in enumerate(enemies_pos)
    ]
    powerups = gen.place_powerups(count=4)

    st.session_state.maze        = maze
    st.session_state.player      = player
    st.session_state.enemies     = enemies
    st.session_state.powerups    = powerups
    st.session_state.exit_pos    = gen.get_exit_position()
    st.session_state.theme       = theme
    st.session_state.game_status = 'playing'
    st.session_state.move_count  = 0
    st.session_state.start_time  = time.time()
    st.session_state.message     = ''
    st.session_state.hints_used  = 0
    st.session_state.show_hint   = False

def draw_maze():
    maze     = st.session_state.maze
    player   = st.session_state.player
    enemies  = st.session_state.enemies
    powerups = st.session_state.powerups
    exit_pos = st.session_state.exit_pos
    theme    = THEME_COLORS.get(
        st.session_state.get('theme', 'Space'),
        THEME_COLORS['Space']
    )

    rows, cols = maze.shape
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor(theme['bg'])
    ax.set_facecolor(theme['bg'])

    for r in range(rows):
        for c in range(cols):
            color = theme['wall'] if maze[r][c] == 1 else theme['path']
            rect  = patches.Rectangle(
                (c, rows - r - 1), 1, 1,
                facecolor=color, edgecolor='none'
            )
            ax.add_patch(rect)

    er, ec = exit_pos
    ax.text(ec + 0.5, rows - er - 0.5, '🚪',
            ha='center', va='center', fontsize=16)

    pu_icons = {
        'map_reveal': '🗺️',
        'speed':      '⚡',
        'shield':     '🛡️',
        'freeze':     '❄️',
        'extra_life': '💚',
    }
    for (pr, pc), ptype in powerups:
        ax.text(pc + 0.5, rows - pr - 0.5,
                pu_icons.get(ptype, '⭐'),
                ha='center', va='center', fontsize=11)

    for enemy in enemies:
        ax.text(enemy.col + 0.5, rows - enemy.row - 0.5,
                enemy.info['emoji'],
                ha='center', va='center', fontsize=13)

    ax.text(player.col + 0.5, rows - player.row - 0.5,
            '🧑', ha='center', va='center', fontsize=15)

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.axis('off')
    plt.tight_layout(pad=0)
    return fig

def get_ai_hint():
    from collections import deque
    maze     = st.session_state.get('maze', None)
    player   = st.session_state.get('player', None)
    exit_pos = st.session_state.get('exit_pos', None)

    if maze is None or player is None or exit_pos is None:
        return "Start a game first!"

    start = player.get_position()
    end   = exit_pos

    queue   = deque([(start, [start])])
    visited = {start}

    while queue:
        (r, c), path = queue.popleft()
        if (r, c) == end:
            if len(path) <= 1:
                return "🚪 You are at the exit!"
            next_step = path[1]
            dr = next_step[0] - start[0]
            dc = next_step[1] - start[1]
            steps = len(path) - 1
            if dr == -1:
                direction = "⬆️ Move UP"
            elif dr == 1:
                direction = "⬇️ Move DOWN"
            elif dc == -1:
                direction = "⬅️ Move LEFT"
            else:
                direction = "➡️ Move RIGHT"
            return f"{direction} — {steps} steps to exit"
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if (0 <= nr < maze.shape[0] and
                0 <= nc < maze.shape[1] and
                maze[nr][nc] == 0 and
                (nr, nc) not in visited):
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))

    return "Keep exploring the maze!"

def handle_move(direction):
    player   = st.session_state.player
    maze     = st.session_state.maze
    enemies  = st.session_state.enemies
    powerups = st.session_state.powerups
    exit_pos = st.session_state.exit_pos

    moved = player.move(direction, maze)
    if moved:
        st.session_state.move_count += 1
        pos = player.get_position()

        for i, (pu_pos, pu_type) in enumerate(powerups):
            if pos == pu_pos:
                msg = player.collect_powerup(pu_type)
                st.session_state.powerups.pop(i)
                st.session_state.message = (
                    f"⚡ {pu_type.replace('_',' ').title()}! {msg}"
                )
                st.session_state.total_powerups = (
                    st.session_state.get('total_powerups', 0) + 1
                )
                if pu_type == 'freeze':
                    for e in enemies:
                        e.freeze()
                break

        for enemy in enemies:
            enemy.move(maze, pos)
            if enemy.touches_player(pos):
                game_over = player.take_damage()
                if game_over:
                    st.session_state.game_status = 'lost'
                    st.session_state.screen = 'game_over'
                    st.session_state.games_played = (
                        st.session_state.get('games_played', 0) + 1
                    )
                    st.session_state.win_streak = 0
                else:
                    st.session_state.message = "💥 Hit! You lost a life!"

        if pos == exit_pos:
            st.session_state.game_status = 'won'
            st.session_state.screen      = 'win'

            moves    = st.session_state.get('move_count', 0)
            elapsed  = int(time.time() -
                          st.session_state.get('start_time', time.time()))
            diff     = st.session_state.get('difficulty', 1)
            coins_earned = max(10, 100 - moves)

            st.session_state.coins = (
                st.session_state.get('coins', 0) + coins_earned
            )
            st.session_state.wins = (
                st.session_state.get('wins', 0) + 1
            )
            st.session_state.games_played = (
                st.session_state.get('games_played', 0) + 1
            )
            st.session_state.total_coins_earned = (
                st.session_state.get('total_coins_earned', 0) + coins_earned
            )

            prev_fastest = st.session_state.get('fastest_time', 9999)
            if elapsed < prev_fastest or prev_fastest == 0:
                st.session_state.fastest_time = elapsed

            st.session_state.win_streak = (
                st.session_state.get('win_streak', 0) + 1
            )
            best = st.session_state.get('best_win_streak', 0)
            if st.session_state.win_streak > best:
                st.session_state.best_win_streak = (
                    st.session_state.win_streak
                )

            if player.lives == 1:
                st.session_state.won_with_one_life = True

            xp_base    = diff * 20
            xp_time    = max(0, 50 - (elapsed // 10))
            xp_moves   = max(0, 30 - (moves // 5))
            xp_earned  = xp_base + xp_time + xp_moves
            st.session_state.xp_earned_last = xp_earned

            total_xp   = st.session_state.get('total_xp', 0) + xp_earned
            st.session_state.total_xp = total_xp

            history = st.session_state.get('game_history', [])
            history.append({
                'Result':    '✅ Win',
                'Level':     diff,
                'Moves':     moves,
                'Time':      f"{elapsed//60:02d}:{elapsed%60:02d}",
                'XP':        xp_earned,
                'Coins':     coins_earned,
            })
            st.session_state.game_history = history[-10:]

    st.rerun()

def show_game():
    if st.session_state.get('new_game', True):
        init_game()
        st.session_state.new_game = False

    player = st.session_state.player

    h1, h2, h3, h4 = st.columns(4)
    h1.write('❤️' * max(player.lives, 0))
    h2.metric("🪙", player.coins)
    elapsed = int(time.time() -
                  st.session_state.get('start_time', time.time()))
    h3.metric("⏱️", f"{elapsed//60:02d}:{elapsed%60:02d}")
    h4.metric("Moves", st.session_state.get('move_count', 0))

    msg = st.session_state.get('message', '')
    if msg:
        st.info(msg)
        st.session_state.message = ''

    st.pyplot(draw_maze(), use_container_width=True)

    if st.session_state.get('show_hint', False):
        hint = st.session_state.get('current_hint', '')
        st.info(f"💡 AI Hint: {hint}")

    _, cu, _ = st.columns([2, 1, 2])
    with cu:
        if st.button("⬆️", use_container_width=True):
            handle_move('UP')

    cl, cm, cr = st.columns(3)
    with cl:
        if st.button("⬅️", use_container_width=True):
            handle_move('LEFT')
    with cm:
        if st.button("⏸️", use_container_width=True):
            st.session_state.screen = 'pause'
            st.rerun()
    with cr:
        if st.button("➡️", use_container_width=True):
            handle_move('RIGHT')

    _, cd, _ = st.columns([2, 1, 2])
    with cd:
        if st.button("⬇️", use_container_width=True):
            handle_move('DOWN')

    st.markdown("---")

    hints_used = st.session_state.get('hints_used', 0)
    max_hints  = 3
    col1, col2 = st.columns(2)
    with col1:
        st.caption(f"💡 Hints: {hints_used}/{max_hints}")
    with col2:
        if hints_used < max_hints:
            if st.button("💡 Get Hint", use_container_width=True):
                hint = get_ai_hint()
                st.session_state.current_hint = hint
                st.session_state.hints_used   = hints_used + 1
                st.session_state.show_hint    = True
                st.rerun()
        else:
            st.caption("No hints left!")

    if player.active_powerups:
        st.caption(
            f"⚡ Active: {', '.join(player.active_powerups)}"
        )

    st.markdown("---")
    if st.button("🏠 Quit to Home", use_container_width=True):
        st.session_state.screen = 'home'
        st.rerun()

def show_win():
    st.balloons()
    st.markdown("## ⭐ ⭐ ⭐  Level Complete!")
    st.markdown("---")

    moves   = st.session_state.get('move_count', 0)
    elapsed = int(time.time() -
                  st.session_state.get('start_time', time.time()))
    coins   = max(10, 100 - moves)
    xp      = st.session_state.get('xp_earned_last', 0)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🪙 Coins",  coins)
    c2.metric("⭐ XP",     xp)
    c3.metric("🎯 Moves",  moves)
    c4.metric("⏱️ Time",
              f"{elapsed//60:02d}:{elapsed%60:02d}")

    if st.session_state.get('level_up_message', ''):
        st.success(st.session_state.level_up_message)
        st.session_state.level_up_message = ''

    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    if col1.button("▶️ Next Level",
                   use_container_width=True,
                   type="primary"):
        st.session_state.difficulty = (
            st.session_state.get('difficulty', 1) + 1
        )
        st.session_state.new_game = True
        st.session_state.screen   = 'game'
        st.rerun()

    if col2.button("🔄 Same Level",
                   use_container_width=True):
        st.session_state.new_game = True
        st.session_state.screen   = 'game'
        st.rerun()

    if col3.button("🏠 Home",
                   use_container_width=True):
        st.session_state.screen = 'home'
        st.rerun()

def show_game_over():
    st.markdown("## 💀 Game Over!")
    st.write("You ran out of lives. Better luck next time!")
    st.markdown("---")

    moves   = st.session_state.get('move_count', 0)
    elapsed = int(time.time() -
                  st.session_state.get('start_time', time.time()))

    c1, c2, c3 = st.columns(3)
    c1.metric("Moves Made", moves)
    c2.metric("Lives Left", 0)
    c3.metric("Time",
              f"{elapsed//60:02d}:{elapsed%60:02d}")

    st.markdown("---")
    col1, col2 = st.columns(2)

    if col1.button("🔄 Try Again",
                   use_container_width=True,
                   type="primary"):
        st.session_state.new_game = True
        st.session_state.screen   = 'game'
        st.rerun()

    if col2.button("🏠 Home",
                   use_container_width=True):
        st.session_state.screen = 'home'
        st.rerun()
