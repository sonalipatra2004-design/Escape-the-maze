import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from game.maze_generator import MazeGenerator
from game.player import Player
from game.enemies import Enemy
from screens.keyboard  import inject_keyboard_controls, show_keyboard_help
from screens.ai_hint   import show_hint_button
from screens.xp_system import award_xp, calculate_game_xp, show_xp_bar
from screens.seasonal  import get_seasonal_colors
import time

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

    enemies_pos  = gen.place_enemies(count=difficulty + 1)
    enemy_types  = ['ghost', 'robot', 'monster', 'spider']
    enemies      = [Enemy(pos, enemy_types[i % len(enemy_types)])
                    for i, pos in enumerate(enemies_pos)]
    powerups     = gen.place_powerups(count=4)

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

def draw_maze():
    maze     = st.session_state.maze
    player   = st.session_state.player
    enemies  = st.session_state.enemies
    powerups = st.session_state.powerups
    exit_pos = st.session_state.exit_pos
    theme    = THEME_COLORS.get(
                 st.session_state.get('theme', 'Space'),
                 THEME_COLORS['Space'])

    rows, cols = maze.shape
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor(theme['bg'])
    ax.set_facecolor(theme['bg'])

    for r in range(rows):
        for c in range(cols):
            color = theme['wall'] if maze[r][c] == 1 else theme['path']
            rect  = patches.Rectangle(
                        (c, rows - r - 1), 1, 1,
                        facecolor=color, edgecolor='none')
            ax.add_patch(rect)

    # Exit door
    er, ec = exit_pos
    ax.text(ec + 0.5, rows - er - 0.5, '🚪',
            ha='center', va='center', fontsize=16)

    # Power-ups
    pu_icons = {
        'map_reveal': '🗺️', 'speed':      '⚡',
        'shield':     '🛡️', 'freeze':     '❄️',
        'extra_life': '💚'
    }
    for (pr, pc), ptype in powerups:
        ax.text(pc + 0.5, rows - pr - 0.5,
                pu_icons.get(ptype, '⭐'),
                ha='center', va='center', fontsize=11)

    # Enemies
    for enemy in enemies:
        ax.text(enemy.col + 0.5, rows - enemy.row - 0.5,
                enemy.info['emoji'],
                ha='center', va='center', fontsize=13)

    # Player
    ax.text(player.col + 0.5, rows - player.row - 0.5,
            '🧑', ha='center', va='center', fontsize=15)

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.axis('off')
    plt.tight_layout(pad=0)
    return fig

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

        # Check power-up collection
        for i, (pu_pos, pu_type) in enumerate(powerups):
            if pos == pu_pos:
                msg = player.collect_powerup(pu_type)
                st.session_state.powerups.pop(i)
                st.session_state.message = f"⚡ {pu_type.replace('_',' ').title()}! {msg}"
                if pu_type == 'freeze':
                    for e in enemies:
                        e.freeze()
                break

        # Move enemies
        for enemy in enemies:
            enemy.move(maze, pos)
            if enemy.touches_player(pos):
                game_over = player.take_damage()
                if game_over:
                    st.session_state.game_status = 'lost'
                    st.session_state.screen = 'game_over'
                    st.session_state.games_played = \
                        st.session_state.get('games_played', 0) + 1
                else:
                    st.session_state.message = "💥 Hit! You lost a life!"

        # Check win
        if pos == exit_pos:
            st.session_state.game_status = 'won'
            st.session_state.screen = 'win'
            coins_earned = max(10, 100 - st.session_state.move_count)
            st.session_state.coins = \
                st.session_state.get('coins', 0) + coins_earned
            st.session_state.wins = \
                st.session_state.get('wins', 0) + 1
            # Award XP on win
import time
elapsed = int(time.time() -
    st.session_state.get('start_time', time.time()))
moves   = st.session_state.get('move_count', 0)
diff    = st.session_state.get('difficulty', 1)
xp_earned = calculate_game_xp(moves, elapsed, diff, True)
leveled_up, new_level = award_xp(xp_earned)
st.session_state.xp_earned_last = xp_earned

# Update statistics
st.session_state.total_coins_earned = \
    st.session_state.get('total_coins_earned', 0) + \
    max(10, 100 - moves)
if elapsed > 0:
    prev_fastest = st.session_state.get('fastest_time', 9999)
    if elapsed < prev_fastest or prev_fastest == 0:
        st.session_state.fastest_time = elapsed

# Win streak
st.session_state.win_streak = \
    st.session_state.get('win_streak', 0) + 1
best = st.session_state.get('best_win_streak', 0)
if st.session_state.win_streak > best:
    st.session_state.best_win_streak = \
        st.session_state.win_streak

# Won with one life check
player = st.session_state.player
if player.lives == 1:
    st.session_state.won_with_one_life = True

# Add to game history
history = st.session_state.get('game_history', [])
history.append({
    'Result':     '✅ Win',
    'Level':      diff,
    'Moves':      moves,
    'Time':       f"{elapsed//60:02d}:{elapsed%60:02d}",
    'XP Earned':  xp_earned,
    'Coins':      max(10, 100 - moves),
})
st.session_state.game_history = history[-10:]
            st.session_state.games_played = \
                st.session_state.get('games_played', 0) + 1

    st.rerun()

def show_game():
    if st.session_state.get('new_game', True):
        init_game()
        st.session_state.new_game = False

    player = st.session_state.player

    # HUD row
    h1, h2, h3, h4 = st.columns(4)
    h1.write('❤️' * max(player.lives, 0))
    h2.metric("🪙", player.coins)
    elapsed = int(time.time() - st.session_state.get('start_time', time.time()))
    h3.metric("⏱️", f"{elapsed//60:02d}:{elapsed%60:02d}")
    h4.metric("Moves", st.session_state.get('move_count', 0))

    # Message banner
    msg = st.session_state.get('message', '')
    if msg:
        st.info(msg)
        st.session_state.message = ''

    # Maze
    st.pyplot(draw_maze(), use_container_width=True)
    
    # Keyboard controls
    inject_keyboard_controls()
    show_keyboard_help()

    # AI Hint button
    show_hint_button()

    # Controls
    large = st.session_state.get('large_ui', False)
    btn_style = "font-size:1.5em;" if large else ""

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
            st.session_state.screen = 'home'
            st.rerun()
    with cr:
        if st.button("➡️", use_container_width=True):
            handle_move('RIGHT')

    _, cd, _ = st.columns([2, 1, 2])
    with cd:
        if st.button("⬇️", use_container_width=True):
            handle_move('DOWN')

    # Active power-ups
    if player.active_powerups:
        st.caption(f"⚡ Active: {', '.join(player.active_powerups)}")

    st.markdown("---")
    if st.button("🏠 Quit to Home"):
        st.session_state.screen = 'home'
        st.rerun()

def show_win():
    st.balloons()
    st.markdown("## ⭐ ⭐ ⭐  Level Complete!")
    st.markdown("---")

    moves   = st.session_state.get('move_count', 0)
    elapsed = int(time.time() - st.session_state.get('start_time', time.time()))
    coins   = max(10, 100 - moves)

    c1, c2, c3 = st.columns(3)
    c1.metric("🪙 Coins Earned", coins)
    c2.metric("🎯 Moves",        moves)
    c3.metric("⏱️ Time",        f"{elapsed//60:02d}:{elapsed%60:02d}")

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    if col1.button("▶️ Next Level", use_container_width=True, type="primary"):
        st.session_state.difficulty = \
            st.session_state.get('difficulty', 1) + 1
        st.session_state.new_game = True
        st.session_state.screen   = 'game'
        st.rerun()
    if col2.button("🔄 Same Level", use_container_width=True):
        st.session_state.new_game = True
        st.session_state.screen   = 'game'
        st.rerun()
    if col3.button("🏠 Home", use_container_width=True):
        st.session_state.screen = 'home'
        st.rerun()

def show_game_over():
    st.markdown("## 💀 Game Over!")
    st.write("You ran out of lives. Better luck next time!")
    st.markdown("---")

    c1, c2, c3 = st.columns(3)
    c1.metric("Moves Made", st.session_state.get('move_count', 0))
    c2.metric("Lives Left", 0)
    elapsed = int(time.time() - st.session_state.get('start_time', time.time()))
    c3.metric("Time",       f"{elapsed//60:02d}:{elapsed%60:02d}")

    st.markdown("---")
    col1, col2 = st.columns(2)
    if col1.button("🔄 Try Again", use_container_width=True, type="primary"):
        st.session_state.new_game = True
        st.session_state.screen   = 'game'
        st.rerun()
    if col2.button("🏠 Home", use_container_width=True):
        st.session_state.screen = 'home'
        st.rerun()
