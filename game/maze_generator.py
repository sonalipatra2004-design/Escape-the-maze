import numpy as np
import random

class MazeGenerator:
    def __init__(self, width=21, height=21):
        self.width = width if width % 2 != 0 else width + 1
        self.height = height if height % 2 != 0 else height + 1
        self.maze = None

    def generate(self, difficulty=1):
        maze = np.ones((self.height, self.width), dtype=int)

        def carve(x, y):
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 < nx < self.height - 1 and 0 < ny < self.width - 1:
                    if maze[nx][ny] == 1:
                        maze[x + dx//2][y + dy//2] = 0
                        maze[nx][ny] = 0
                        carve(nx, ny)

        maze[1][1] = 0
        carve(1, 1)
        maze[1][0] = 0
        maze[self.height-2][self.width-1] = 0

        self.maze = maze
        return maze

    def get_start_position(self):
        return (1, 1)

    def get_exit_position(self):
        return (self.height - 2, self.width - 2)

    def place_enemies(self, count=3):
        open_cells = list(zip(*np.where(self.maze == 0)))
        open_cells = [c for c in open_cells if c not in
                      [self.get_start_position(), self.get_exit_position()]]
        return random.sample(open_cells, min(count, len(open_cells)))

    def place_powerups(self, count=4):
        open_cells = list(zip(*np.where(self.maze == 0)))
        open_cells = [c for c in open_cells if c not in
                      [self.get_start_position(), self.get_exit_position()]]
        powerup_types = ['map_reveal', 'speed', 'shield', 'freeze', 'extra_life']
        positions = random.sample(open_cells, min(count, len(open_cells)))
        return [(pos, random.choice(powerup_types)) for pos in positions]
