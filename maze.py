import random


class Maze:
    def __init__(self, size):
        self.size = size
        self.grid = self.generate()

    def generate(self):
        grid = [[1] * self.size for _ in range(self.size)]
        self.carve(grid, 1, 1)
        return grid

    def carve(self, grid, x, y):
        grid[y][x] = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < self.size and 0 <= ny < self.size and grid[ny][nx] == 1:
                grid[y + dy][x + dx] = 0
                self.carve(grid, nx, ny)

    def getEmptyTile(self):
        emptyTiles = []
        for y in range(self.size):
            for x in range(self.size):
                if self.grid[y][x] == 0:
                    emptyTiles.append((x, y))
        return random.choice(emptyTiles)
