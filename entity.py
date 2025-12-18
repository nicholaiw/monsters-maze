from config import TileType


class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, maze):
        pass


class Door(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)


class Character(Entity):
    def __init__(self, x, y, role, controller, moveDelay):
        super().__init__(x, y)
        self.role = role
        self.controller = controller
        self.moveDelay = {"delay": moveDelay, "counter": 0}
        self.direction = None

    def update(self, maze):
        newDirection = self.controller.getDirection(self, maze)
        if newDirection is not None:
            self.direction = newDirection

        self._move(maze)

    def _move(self, maze):
        self.moveDelay["counter"] -= 1

        if self.moveDelay["counter"] > 0 or self.direction is None:
            return

        dx, dy = self.direction
        nx, ny = self.x + dx, self.y + dy

        if self._isWalkable(nx, ny, maze):
            self.x, self.y = nx, ny
            self.moveDelay["counter"] = self.moveDelay["delay"]

    def _isWalkable(self, x, y, maze):
        return (
            0 <= x < maze.size
            and 0 <= y < maze.size
            and maze.grid[y][x] != TileType.WALL
        )
