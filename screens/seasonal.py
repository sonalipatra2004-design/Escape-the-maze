import streamlit as st
from datetime import date

def get_current_season():
    """Auto detect season based on current date"""
    today = date.today()
    month = today.month
    day   = today.day

    if month == 10:
        return 'halloween'
    elif month == 12:
        return 'christmas'
    elif month == 11 and 1 <= day <= 15:
        return 'diwali'
    elif month == 1 and day <= 7:
        return 'newyear'
    elif month in [6, 7, 8]:
        return 'summer'
    elif month in [3, 4]:
        return 'spring'
    else:
        return 'normal'

SEASONAL_THEMES = {
    'halloween': {
        'name':       '🎃 Halloween',
        'emoji':      '🎃',
        'wall':       '#2d0a0a',
        'path':       '#ff6600',
        'bg':         '#1a0000',
        'text_color': '#ff6600',
        'greeting':   'Happy Halloween! 👻',
        'bonus':      'Double XP this month!',
        'icon':       '🦇',
    },
    'christmas': {
        'name':       '🎄 Christmas',
        'emoji':      '🎄',
        'wall':       '#0d3b0d',
        'path':       '#ff0000',
        'bg':         '#001a00',
        'text_color': '#ff0000',
        'greeting':   'Merry Christmas! 🎅',
        'bonus':      'Triple daily rewards!',
        'icon':       '⛄',
    },
    'diwali': {
        'name':       '🪔 Diwali',
        'emoji':      '🪔',
        'wall':       '#3d1a00',
        'path':       '#ffd700',
        'bg':         '#1a0a00',
        'text_color': '#ffd700',
        'greeting':   'Happy Diwali! 🪔',
        'bonus':      'Golden coins x3!',
        'icon':       '✨',
    },
    'newyear': {
        'name':       '🎆 New Year',
        'emoji':      '🎆',
        'wall':       '#1a1a2e',
        'path':       '#gold',
        'bg':         '#0a0a1e',
        'text_color': '#ffd700',
        'greeting':   'Happy New Year! 🥂',
        'bonus':      'Special new year rewards!',
        'icon':       '🎇',
    },
    'summer': {
        'name':       '☀️ Summer',
        'emoji':      '☀️',
        'wall':       '#8B6914',
        'path':       '#87CEEB',
        'bg':         '#001a33',
        'text_color': '#FFD700',
        'greeting':   'Hot Summer Maze! ☀️',
        'bonus':      'Summer speed boost!',
        'icon':       '🌊',
    },
    'spring': {
        'name':       '🌸 Spring',
        'emoji':      '🌸',
        'wall':       '#2d5a1b',
        'path':       '#90EE90',
        'bg':         '#0a1a0a',
        'text_color': '#00cc44',
        'greeting':   'Spring is here! 🌸',
        'bonus':      'Flower power ups!',
        'icon':       '🌺',
    },
    'normal': {
        'name':       '🚀 Normal',
        'emoji':      '🚀',
        'wall':       '#37474F',
        'path':       '#B0BEC5',
        'bg':         '#0A0A2E',
        'text_color': '#00FFFF',
        'greeting':   'Welcome to AI Maze!',
        'bonus':      '',
        'icon':       '⭐',
    },
}

def get_seasonal_colors():
    """Get maze colors for current season"""
    manual = st.session_state.get('manual_theme', None)
    if manual and manual in SEASONAL_THEMES:
        return SEASONAL_THEMES[manual]
    season = get_current_season()
    return SEASONAL_THEMES.get(season, SEASONAL_THEMES['normal'])

def show_seasonal_banner():
    """Show seasonal greeting on home screen"""
    theme = get_seasonal_colors()
    if theme['greeting']:
        st.markdown(
            f"<div style='text-align:center; "
            f"color:{theme['text_color']}; "
            f"font-size:1.3em; font-weight:bold;'>"
            f"{theme['icon']} {theme['greeting']}</div>",
            unsafe_allow_html=True)
        if theme['bonus']:
            st.success(f"🎁 Special Event: {theme['bonus']}")

def show_seasonal_settings():
    """Theme selector in settings"""
    st.subheader("🎨 Seasonal Theme")
    current = get_current_season()
    auto_theme = SEASONAL_THEMES[current]
    st.info(f"Auto theme: **{auto_theme['name']}** "
            f"(based on today's date)")

    st.write("Or choose manually:")
    theme_options = {v['name']: k
                     for k, v in SEASONAL_THEMES.items()}
    selected = st.selectbox(
        "Manual Theme Override",
        ['Auto (recommended)'] + list(theme_options.keys()))

    if selected == 'Auto (recommended)':
        st.session_state.manual_theme = None
    else:
        st.session_state.manual_theme = theme_options[selected]

    # Preview
    theme = get_seasonal_colors()
    st.markdown(
        f"<div style='background:{theme['bg']}; "
        f"padding:15px; border-radius:10px; "
        f"text-align:center;'>"
        f"<span style='color:{theme['text_color']}; "
        f"font-size:2em;'>{theme['icon']}</span><br>"
        f"<span style='color:{theme['text_color']};'>"
        f"{theme['name']} Preview</span></div>",
        unsafe_allow_html=True)
