import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time
from game.maze_generator import MazeGenerator
from game.player import Player
from game.enemies import Enemy

THEME_COLORS = {
    'Forest':  {'wall': '#1a5c1a', 'path': '#c8f0c8', 'bg': '#0a2e0a'},
    'Desert':  {'wall': '#8B6914', 'path': '#F4D03F', 'bg': '#5D4037'},
    'Ice':     {'wall': '#4FC3F7', 'path': '#E3F2FD', 'bg': '#0D47A1'},
    'Lava':    {'wall': '#BF360C', 'path': '#FF8F00', 'bg': '#3E2723'},
    'Space':   {'wall': '#222244', 'path': '#e0e0ff', 'bg': '#0A0A2E'},
    'Haunted': {'wall': '#4A0080', 'path': '#CE93D8', 'bg': '#1A0030'},
}

def init_game():
    difficulty = st.session_state.get('difficulty', 1)
    theme      = st.session_state.get('theme', 'Space')
    size       = 11 + (difficulty * 2)

    gen    = MazeGenerator(size, size)
    maze   = gen.generate(difficulty)
    player = Player(gen.get_start_position())

    enemies_pos = gen.place_enemies(count=difficulty)
    enemy_types = ['ghost', 'robot', 'monster', 'spider']
    enemies = [
        Enemy(pos, enemy_types[i % len(enemy_types)])
        for i, pos in enumerate(enemies_pos)
    ]
    powerups = gen.place_powerups(count=3)

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
    st.session_state.last_move   = None

def draw_maze_image():
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

    # Use a fixed DPI and size so image never changes size
    fig, ax = plt.subplots(figsize=(6, 6), dpi=80)
    fig.patch.set_facecolor(theme['bg'])
    ax.set_facecolor(theme['bg'])

    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 1:
                rect = patches.Rectangle(
                    (c, rows - r - 1), 1, 1,
                    facecolor=theme['wall'],
                    edgecolor='none'
                )
            else:
                rect = patches.Rectangle(
                    (c, rows - r - 1), 1, 1,
                    facecolor=theme['path'],
                    edgecolor='#dddddd',
                    linewidth=0.2
                )
            ax.add_patch(rect)

    # START marker
    ax.text(1.5, rows - 1 - 0.5, 'START',
            ha='center', va='center',
            fontsize=4, color='green',
            fontweight='bold')

    # EXIT — bright green box
    er, ec = exit_pos
    exit_rect = patches.Rectangle(
        (ec, rows - er - 1), 1, 1,
        facecolor='#00DD00',
        edgecolor='#FFFF00',
        linewidth=2
    )
    ax.add_patch(exit_rect)
    ax.text(ec + 0.5, rows - er - 0.5, '🚪',
            ha='center', va='center', fontsize=13)

    # Power-ups
    pu_colors = {
        'map_reveal': '#FFD700',
        'speed':      '#FF6600',
        'shield':     '#0066FF',
        'freeze':     '#00CCFF',
        'extra_life': '#FF0066',
    }
    pu_icons = {
        'map_reveal': '🗺️',
        'speed':      '⚡',
        'shield':     '🛡️',
        'freeze':     '❄️',
        'extra_life': '💚',
    }
    for (pr, pc), ptype in powerups:
        bg = patches.Circle(
            (pc + 0.5, rows - pr - 0.5), 0.33,
            facecolor=pu_colors.get(ptype, '#FFFF00'),
            alpha=0.8
        )
        ax.add_patch(bg)
        ax.text(pc + 0.5, rows - pr - 0.5,
                pu_icons.get(ptype, '⭐'),
                ha='center', va='center', fontsize=9)

    # Enemies
    for enemy in enemies:
        warn = patches.Circle(
            (enemy.col + 0.5, rows - enemy.row - 0.5), 0.38,
            facecolor='#FF0000', alpha=0.3
        )
        ax.add_patch(warn)
        ax.text(enemy.col + 0.5, rows - enemy.row - 0.5,
                enemy.info['emoji'],
                ha='center', va='center', fontsize=12)

    # Player — bright green circle behind
    player_bg = patches.Circle(
        (player.col + 0.5, rows - player.row - 0.5), 0.4,
        facecolor='#00FF00', alpha=0.6
    )
    ax.add_patch(player_bg)
    ax.text(player.col + 0.5, rows - player.row - 0.5,
            '🧑', ha='center', va='center', fontsize=14)

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect('equal')
    ax.axis('off')

    # Remove all padding/margins
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    return fig

def get_ai_hint():
    from collections import deque
    maze     = st.session_state.get('maze', None)
    player   = st.session_state.get('player', None)
    exit_pos = st.session_state.get('exit_pos', None)
    if maze is None or player is None or exit_pos is None:
        return "Start a game first!"
    start   = player.get_position()
    end     = exit_pos
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
            if dr == -1:   direction = "⬆️ Move UP"
            elif dr == 1:  direction = "⬇️ Move DOWN"
            elif dc == -1: direction = "⬅️ Move LEFT"
            else:          direction = "➡️ Move RIGHT"
            return f"{direction} — {steps} steps to exit"
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if (0 <= nr < maze.shape[0] and
                0 <= nc < maze.shape[1] and
                maze[nr][nc] == 0 and
                (nr, nc) not in visited):
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))
    return "Keep exploring!"

def process_move(direction):
    """Process move logic WITHOUT calling st.rerun()"""
    player   = st.session_state.player
    maze     = st.session_state.maze
    enemies  = st.session_state.enemies
    powerups = st.session_state.powerups
    exit_pos = st.session_state.exit_pos

    moved = player.move(direction, maze)
    if not moved:
        st.session_state.message = "🧱 Wall! Try a different direction."
        return

    st.session_state.move_count += 1
    st.session_state.message = ''
    pos = player.get_position()

    # Power-up collection
    for i, (pu_pos, pu_type) in enumerate(powerups):
        if pos == pu_pos:
            msg = player.collect_powerup(pu_type)
            st.session_state.powerups.pop(i)
            st.session_state.message = (
                f"⚡ Got {pu_type.replace('_',' ').title()}! {msg}"
            )
            st.session_state.total_powerups = (
                st.session_state.get('total_powerups', 0) + 1
            )
            if pu_type == 'freeze':
                for e in enemies:
                    e.freeze()
            break

    # Enemy movement
    for enemy in enemies:
        enemy.move(maze, pos)
        if enemy.touches_player(pos):
            game_over = player.take_damage()
            if game_over:
                st.session_state.game_status  = 'lost'
                st.session_state.screen       = 'game_over'
                st.session_state.games_played = (
                    st.session_state.get('games_played', 0) + 1
                )
                st.session_state.win_streak = 0
                return
            else:
                st.session_state.message = (
                    f"💥 Enemy hit you! {player.lives} lives left!"
                )

    # Check win
    if pos == exit_pos:
        st.session_state.game_status = 'won'
        st.session_state.screen      = 'win'
        moves        = st.session_state.get('move_count', 0)
        elapsed      = int(time.time() -
                           st.session_state.get('start_time', time.time()))
        diff         = st.session_state.get('difficulty', 1)
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
        xp_earned = (
            (diff * 20) +
            max(0, 50 - (elapsed // 10)) +
            max(0, 30 - (moves // 5))
        )
        st.session_state.xp_earned_last = xp_earned
        st.session_state.total_xp = (
            st.session_state.get('total_xp', 0) + xp_earned
        )
        history = st.session_state.get('game_history', [])
        history.append({
            'Result': '✅ Win',
            'Level':  diff,
            'Moves':  moves,
            'Time':   f"{elapsed//60:02d}:{elapsed%60:02d}",
            'XP':     xp_earned,
            'Coins':  coins_earned,
        })
        st.session_state.game_history = history[-10:]

@st.fragment
def game_fragment():
    """
    This fragment reruns ONLY itself — not the whole page.
    This stops the blinking/squeezing effect completely.
    """
    player = st.session_state.player

    # ── HUD ──────────────────────────────────────
    h1, h2, h3, h4 = st.columns(4)
    h1.write('❤️' * max(player.lives, 0) or '💀')
    h2.metric("🪙", player.coins)
    elapsed = int(time.time() -
                  st.session_state.get('start_time', time.time()))
    h3.metric("⏱️", f"{elapsed//60:02d}:{elapsed%60:02d}")
    h4.metric("🎯", st.session_state.get('move_count', 0))

    # ── MESSAGE ──────────────────────────────────
    msg = st.session_state.get('message', '')
    if msg:
        st.warning(msg)

    # ── HINT ─────────────────────────────────────
    if st.session_state.get('show_hint', False):
        st.success(
            f"💡 {st.session_state.get('current_hint', '')}"
        )

    # ── MAZE IMAGE ───────────────────────────────
    fig = draw_maze_image()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    # ── GOAL REMINDER ────────────────────────────
    st.info("🎯 Goal: Reach the 🚪 GREEN door to WIN!")

    # ── CONTROL BUTTONS ──────────────────────────
    st.markdown("#### 🕹️ Move")

    _, cu, _ = st.columns([2, 1, 2])
    with cu:
        up = st.button("⬆️", use_container_width=True,
                       key="btn_up")

    cl, cm, cr = st.columns(3)
    with cl:
        left = st.button("⬅️", use_container_width=True,
                         key="btn_left")
    with cm:
        pause = st.button("⏸️", use_container_width=True,
                          key="btn_pause")
    with cr:
        right = st.button("➡️", use_container_width=True,
                          key="btn_right")

    _, cd, _ = st.columns([2, 1, 2])
    with cd:
        down = st.button("⬇️", use_container_width=True,
                         key="btn_down")

    # Process button presses
    if up:
        process_move('UP')
        st.rerun(scope="fragment")
    if down:
        process_move('DOWN')
        st.rerun(scope="fragment")
    if left:
        process_move('LEFT')
        st.rerun(scope="fragment")
    if right:
        process_move('RIGHT')
        st.rerun(scope="fragment")
    if pause:
        st.session_state.screen = 'pause'
        st.rerun()

    # ── HINT BUTTON ──────────────────────────────
    st.markdown("---")
    hints_used = st.session_state.get('hints_used', 0)
    max_hints  = 3
    col1, col2 = st.columns(2)
    with col1:
        if hints_used < max_hints:
            if st.button(
                f"💡 Hint ({max_hints-hints_used} left)",
                use_container_width=True,
                key="btn_hint"
            ):
                hint = get_ai_hint()
                st.session_state.current_hint = hint
                st.session_state.hints_used   = hints_used + 1
                st.session_state.show_hint    = True
                st.rerun(scope="fragment")
        else:
            st.caption("💡 No hints left!")
    with col2:
        if st.button("🏠 Home",
                     use_container_width=True,
                     key="btn_home"):
            st.session_state.screen = 'home'
            st.rerun()

    # Active power-ups
    if player.active_powerups:
        st.success(
            f"⚡ Active: {', '.join(player.active_powerups)}"
        )

    # Quick rules
    with st.expander("❓ How to play"):
        st.markdown("""
        1. 🧑 = You. Move using arrow buttons above
        2. Light cells = paths ✅ Dark cells = walls ❌
        3. Reach 🚪 green door = WIN!
        4. Avoid 👻🤖 enemies or lose ❤️
        5. Collect ⚡🛡️❄️💚 power-ups for help
        6. Tap 💡 Hint if stuck!
        """)

    # Check if game ended — redirect whole page
    if st.session_state.get('screen') in ['win', 'game_over']:
        st.rerun()

def show_game():
    if st.session_state.get('new_game', True):
        init_game()
        st.session_state.new_game = False

    # Legend above the fragment
    st.markdown("""
    🧑 You &nbsp;|&nbsp;
    🚪 EXIT &nbsp;|&nbsp;
    👻🤖 Enemy &nbsp;|&nbsp;
    ⚡🛡️❄️💚 Power-up
    """)

    # Call the fragment — only THIS reruns on button click
    game_fragment()

def show_win():
    st.balloons()
    st.markdown("## ⭐ ⭐ ⭐ Level Complete!")
    st.success("🎉 You escaped the maze!")
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
    if col2.button("🔄 Replay",
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
    st.error("You ran out of lives! Try again!")
    st.markdown("---")
    moves   = st.session_state.get('move_count', 0)
    elapsed = int(time.time() -
                  st.session_state.get('start_time', time.time()))
    c1, c2, c3 = st.columns(3)
    c1.metric("Moves", moves)
    c2.metric("Lives", 0)
    c3.metric("Time",
              f"{elapsed//60:02d}:{elapsed%60:02d}")
    st.info("💡 Tip: Use 💡 hints and ⚡ power-ups next time!")
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
