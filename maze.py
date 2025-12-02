import random
from constant import TileType


class Maze:
    def __init__(self, size):
        self.size = size
        self.grid = self._generate()

    def _generate(self):
        grid = [[TileType.WALL] * self.size for _ in range(self.size)]
        self._carve(grid, 1, 1)
        return grid

    def _carve(self, grid, x, y):
        grid[y][x] = TileType.FLOOR

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2

            if (
                0 <= nx < self.size
                and 0 <= ny < self.size
                and grid[ny][nx] == TileType.WALL
            ):
                grid[y + dy][x + dx] = TileType.FLOOR
                self._carve(grid, nx, ny)

    def getEmptyTile(self):
        emptyTiles = [
            (x, y)
            for y in range(self.size)
            for x in range(self.size)
            if self.grid[y][x] == TileType.FLOOR
        ]
        return random.choice(emptyTiles) if emptyTiles else (1, 1)

    def isWalkable(self, x, y):
        return (
            0 <= x < self.size
            and 0 <= y < self.size
            and self.grid[y][x] == TileType.FLOOR
        )
