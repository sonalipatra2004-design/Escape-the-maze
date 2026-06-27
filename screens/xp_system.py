import streamlit as st

LEVEL_THRESHOLDS = [
    0, 100, 250, 450, 700, 1000,
    1350, 1750, 2200, 2700, 3250,
    3850, 4500, 5200, 5950, 6750,
    7600, 8500, 9450, 10450, 11500,
]

LEVEL_TITLES = [
    'Newbie', 'Beginner', 'Explorer', 'Adventurer',
    'Maze Walker', 'Maze Runner', 'Maze Hunter',
    'Maze Master', 'Shadow Runner', 'Ghost Chaser',
    'Speed Demon', 'Trap Dodger', 'Elite Runner',
    'Maze Legend', 'Grand Master', 'Maze God',
    'Immortal', 'Phantom', 'Titan', 'Champion',
    'AI Maze King',
]

def get_level_from_xp(xp):
    level = 1
    for i, threshold in enumerate(LEVEL_THRESHOLDS):
        if xp >= threshold:
            level = i + 1
    return min(level, len(LEVEL_TITLES))

def get_xp_for_next_level(current_level):
    if current_level >= len(LEVEL_THRESHOLDS):
        return LEVEL_THRESHOLDS[-1]
    return LEVEL_THRESHOLDS[current_level]

def get_level_title(level):
    idx = min(level - 1, len(LEVEL_TITLES) - 1)
    return LEVEL_TITLES[idx]

def award_xp(amount, reason=""):
    """Award XP and check for level up"""
    current_xp    = st.session_state.get('total_xp', 0)
    current_level = get_level_from_xp(current_xp)

    new_xp    = current_xp + amount
    new_level = get_level_from_xp(new_xp)

    st.session_state.total_xp     = new_xp
    st.session_state.player_level = new_level
    st.session_state.xp           = new_xp

    # Level up!
    if new_level > current_level:
        bonus_coins = new_level * 50
        st.session_state.coins = \
            st.session_state.get('coins', 0) + bonus_coins
        st.session_state.level_up_message = (
            f"🎉 LEVEL UP! You are now Level {new_level} "
            f"— {get_level_title(new_level)}! "
            f"+{bonus_coins} bonus coins!"
        )
        return True, new_level
    return False, new_level

def calculate_game_xp(moves, time_seconds, difficulty, won):
    """Calculate XP earned from a game"""
    if not won:
        return max(5, difficulty * 3)

    base_xp   = difficulty * 20
    time_bonus = max(0, 50 - (time_seconds // 10))
    move_bonus = max(0, 30 - (moves // 5))
    total_xp  = base_xp + time_bonus + move_bonus
    return total_xp

def show_xp_bar():
    """Show XP progress bar — use in profile and game screens"""
    total_xp = st.session_state.get('total_xp', 0)
    level    = get_level_from_xp(total_xp)
    title    = get_level_title(level)

    current_threshold = LEVEL_THRESHOLDS[
        min(level - 1, len(LEVEL_THRESHOLDS) - 1)]
    next_threshold = get_xp_for_next_level(level)

    xp_in_level   = total_xp - current_threshold
    xp_needed     = next_threshold - current_threshold
    progress      = min(xp_in_level / max(xp_needed, 1), 1.0)

    st.markdown(f"**Level {level} — {title}**")
    st.progress(progress,
                text=f"XP: {xp_in_level}/{xp_needed} to next level")
