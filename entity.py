class Entity:
    def __init__(self, x, y, symbol, collision, view=1):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.collision = collision
        self.view = view


class Character(Entity):
    directions = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}

    def move(self, direction, entities):

        if direction == None:
            return

        dx, dy = Character.directions[direction]
        newX = self.x + dx
        newY = self.y + dy


        for entity in entities:
            if entity.collision and entity.x == newX and entity.y == newY:
                return

        self.x = newX
        self.y = newY


class Wall(Entity):
    pass