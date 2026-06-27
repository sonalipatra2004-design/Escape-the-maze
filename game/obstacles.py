import random

OBSTACLE_TYPES = {
    'fire':          {'emoji': '🔥', 'damage': True,  'description': 'Burns on contact'},
    'ice_floor':     {'emoji': '🧊', 'damage': False, 'description': 'Slide 2 steps'},
    'poison':        {'emoji': '☠️', 'damage': True,  'description': 'Lose 1 life slowly'},
    'laser':         {'emoji': '🔴', 'damage': True,  'description': 'Instant hit'},
    'falling_rocks': {'emoji': '🪨', 'damage': True,  'description': 'Random drop'},
    'moving_wall':   {'emoji': '⬜', 'damage': False, 'description': 'Pushes player'},
    'locked_door':   {'emoji': '🔒', 'damage': False, 'description': 'Needs a key'},
    'hidden_path':   {'emoji': '👁️', 'damage': False, 'description': 'Invisible until stepped on'},
}

def place_obstacles(maze, count=3):
    """Place random obstacles on open cells"""
    import numpy as np
    open_cells = list(zip(*np.where(maze == 0)))
    obstacle_keys = list(OBSTACLE_TYPES.keys())
    selected = random.sample(open_cells, min(count, len(open_cells)))
    return [(pos, random.choice(obstacle_keys)) for pos in selected]

def get_obstacle_info(obstacle_type):
    return OBSTACLE_TYPES.get(obstacle_type, {})
