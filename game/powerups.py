POWERUP_INFO = {
    'map_reveal': {
        'emoji': '🗺️',
        'name': 'Map Reveal',
        'description': 'See the full maze for 30 seconds',
        'duration': 30,
        'price': 50
    },
    'speed': {
        'emoji': '⚡',
        'name': 'Speed Boost',
        'description': 'Move twice per turn for 20 seconds',
        'duration': 20,
        'price': 30
    },
    'shield': {
        'emoji': '🛡️',
        'name': 'Shield',
        'description': 'Block one enemy hit',
        'duration': 0,
        'price': 40
    },
    'freeze': {
        'emoji': '❄️',
        'name': 'Freeze Enemies',
        'description': 'Stop all enemies for 15 seconds',
        'duration': 15,
        'price': 60
    },
    'extra_life': {
        'emoji': '💚',
        'name': 'Extra Life',
        'description': 'Gain one additional life',
        'duration': 0,
        'price': 80
    },
    'teleport': {
        'emoji': '🌀',
        'name': 'Teleport',
        'description': 'Jump to a random open cell',
        'duration': 0,
        'price': 70
    },
    'double_coins': {
        'emoji': '🪙',
        'name': 'Double Coins',
        'description': 'Earn 2x coins for 60 seconds',
        'duration': 60,
        'price': 45
    },
    'trap_detector': {
        'emoji': '🔍',
        'name': 'Trap Detector',
        'description': 'Highlights all traps on the maze',
        'duration': 25,
        'price': 55
    },
}

def get_powerup_info(powerup_type):
    return POWERUP_INFO.get(powerup_type, {})

def get_all_powerups():
    return POWERUP_INFO
