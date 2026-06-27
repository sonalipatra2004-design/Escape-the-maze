class Player:
    def __init__(self, start_pos):
        self.row, self.col = start_pos
        self.lives = 3
        self.coins = 0
        self.score = 0
        self.has_shield = False
        self.speed_boost = False
        self.active_powerups = []

    def move(self, direction, maze):
        moves = {
            'UP':    (-1, 0),
            'DOWN':  (1,  0),
            'LEFT':  (0, -1),
            'RIGHT': (0,  1)
        }
        dr, dc = moves.get(direction, (0, 0))
        new_row = self.row + dr
        new_col = self.col + dc
        rows, cols = maze.shape
        if 0 <= new_row < rows and 0 <= new_col < cols:
            if maze[new_row][new_col] == 0:
                self.row = new_row
                self.col = new_col
                return True
        return False

    def collect_powerup(self, powerup_type):
        powerup_effects = {
            'map_reveal': 'Reveals full map for 30s',
            'speed':      'Move twice per turn for 20s',
            'shield':     'Immune to one enemy hit',
            'freeze':     'Freezes all enemies for 15s',
            'extra_life': '+1 Life added'
        }
        self.active_powerups.append(powerup_type)
        if powerup_type == 'shield':
            self.has_shield = True
        elif powerup_type == 'extra_life':
            self.lives += 1
        return powerup_effects.get(powerup_type, '')

    def take_damage(self):
        if self.has_shield:
            self.has_shield = False
            return False
        self.lives -= 1
        return self.lives <= 0

    def get_position(self):
        return (self.row, self.col)
