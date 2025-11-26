import random

from entity import Character, Wall


class Map:
    def __init__(self, size=15):
        self.size = size
        self.entities = []

        self.generateMaze()

        self.player = Character(0, 0, "@", False, 5)
        self.spawnEntity(self.player)

    def generateMaze(self):
        maze = [[1] * self.size for _ in range(self.size)]

        def carve(x, y):
            maze[y][x] = 0
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = x + dx * 2, y + dy * 2
                if 0 <= nx < self.size and 0 <= ny < self.size and maze[ny][nx]:
                    maze[y + dy][x + dx] = 0
                    carve(nx, ny)

        carve(1, 1)

        for y in range(self.size):
            for x in range(self.size):
                if maze[y][x] == 1:
                    self.entities.append(Wall(x, y, "#", True))

    def spawnEntity(self, entity):
        positions = []
        for y in range(self.size):
            for x in range(self.size):
                occupied = any(e.x == x and e.y == y for e in self.entities)
                if not occupied:
                    positions.append((x, y))

        entity.x, entity.y = random.choice(positions)
        self.entities.append(entity)
