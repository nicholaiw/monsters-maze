class Entity:
    def __init__(self, x, y, symbol, collision, view=1):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.collision = collision
        self.view = view


class Character(Entity):
    directions = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}

    def move(self, direction, view):

        if direction is not None:

            movement = Character.directions[direction]

            newX = self.x + movement[0]
            newY = self.y + movement[1]

            for entity in view:
                if entity.collision and entity.x == newX and entity.y == newY:
                    return

            self.x = newX
            self.y = newY


class Wall(Entity):
    pass
