from constant import TileType


class GameObject:
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol

    def update(self, game):
        pass


class Character(GameObject):
    def __init__(self, x, y, symbol, role, controller):
        super().__init__(x, y, symbol)
        self.role = role
        self.controller = controller

    def update(self, game):
        direction = self.controller.getDirection(self, game.gameObjects, game.maze)
        self._move(direction, game.maze, game.gameObjects)

    def _move(self, direction, maze, gameObjects):
        if direction is None:
            return

        dx, dy = direction
        nx, ny = self.x + dx, self.y + dy

        if not self._isValidPosition(nx, ny, maze, gameObjects):
            return

        self.x, self.y = nx, ny

    def _isValidPosition(self, x, y, maze, gameObjects):
        if not (0 <= x < maze.size and 0 <= y < maze.size):
            return False

        if maze.grid[y][x] == TileType.WALL:
            return False

        return True
