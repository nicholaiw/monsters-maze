class GameObject:
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol


class Character(GameObject):
    directions = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}

    def __init__(self, x, y, symbol, role):
        super().__init__(x, y, symbol)
        self.role = role

    def move(self, direction, maze):
        if direction is None:
            return
        dx, dy = Character.directions[direction]
        nx, ny = self.x + dx, self.y + dy
        if maze[ny][nx] == 1:
            return
        self.x, self.y = nx, ny
