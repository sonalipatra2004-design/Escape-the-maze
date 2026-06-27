import random
from collections import deque

class Enemy:
    TYPES = {
        'ghost':   {'emoji': '👻', 'speed': 1, 'smart': True},
        'robot':   {'emoji': '🤖', 'speed': 1, 'smart': True},
        'monster': {'emoji': '👹', 'speed': 1, 'smart': False},
        'spider':  {'emoji': '🕷️', 'speed': 2, 'smart': False},
    }

    def __init__(self, position, enemy_type='ghost'):
        self.row, self.col = position
        self.type = enemy_type
        self.info = self.TYPES.get(enemy_type, self.TYPES['ghost'])
        self.frozen = False

    def move(self, maze, player_pos):
        if self.frozen:
            return
        if self.info['smart']:
            self._move_toward_player(maze, player_pos)
        else:
            self._move_random(maze)

    def _move_toward_player(self, maze, player_pos):
        target = player_pos
        start = (self.row, self.col)
        queue = deque([(start, [start])])
        visited = {start}
        while queue:
            (r, c), path = queue.popleft()
            if (r, c) == target:
                if len(path) > 1:
                    self.row, self.col = path[1]
                return
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r+dr, c+dc
                if (0 <= nr < maze.shape[0] and 0 <= nc < maze.shape[1]
                        and maze[nr][nc] == 0 and (nr,nc) not in visited):
                    visited.add((nr,nc))
                    queue.append(((nr,nc), path+[(nr,nc)]))

    def _move_random(self, maze):
        directions = [(-1,0),(1,0),(0,-1),(0,1)]
        random.shuffle(directions)
        for dr, dc in directions:
            nr, nc = self.row+dr, self.col+dc
            if (0 <= nr < maze.shape[0] and 0 <= nc < maze.shape[1]
                    and maze[nr][nc] == 0):
                self.row, self.col = nr, nc
                break

    def touches_player(self, player_pos):
        return (self.row, self.col) == player_pos

    def freeze(self):
        self.frozen = True

    def unfreeze(self):
        self.frozen = False
