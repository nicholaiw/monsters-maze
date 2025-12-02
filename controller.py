import random
from collections import deque
from pynput import keyboard


class KeyboardController:
    def __init__(self, bindings):
        self.bindings = bindings
        self.direction = None
        self.listener = keyboard.Listener(on_release=self.getKey)
        self.listener.start()

    def getKey(self, key):
        self.direction = self.bindings.get(key, None)

    def getDirection(self):
        return self.direction


class AiMonster:
    directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]

    def __init__(self, character, view, maze, gameObjects):
        self.character = character
        self.view = view
        self.maze = maze
        self.gameObjects = gameObjects
        self.direction = None
        self.target = None
        self.visited = {}

    def getDirection(self):
        self.updateVisited()
        self.visibleHuman()

        if self.target and (self.character.x, self.character.y) == (
            self.target.x,
            self.target.y,
        ):
            self.target = None

        if self.target:
            self.pathfind((self.target.x, self.target.y))
            return self.direction
        else:
            self.pathfind(self.leastVisited())
            return self.direction

    def visibleHuman(self):
        for obj in self.gameObjects:
            if getattr(obj, "role", None) == "human":
                if (
                    abs(obj.x - self.character.x) + abs(obj.y - self.character.y)
                    <= self.view
                ):
                    self.target = obj

    def updateVisited(self):
        position = (self.character.x, self.character.y)
        self.visited[position] = self.visited.get(position, 0) + 1

    def leastVisited(self):
        tiles = []

        for dx, dy in self.directions:
            nx, ny = self.character.x + dx, self.character.y + dy

            if self.walkable(nx, ny):
                visits = self.visited.get((nx, ny), 0)
                tiles.append(((nx, ny), visits))

        if not tiles:
            return (self.character.x, self.character.y)

        minVisits = min(tile[1] for tile in tiles)
        minTiles = [tile[0] for tile in tiles if tile[1] == minVisits]
        return random.choice(minTiles)

    def walkable(self, x, y):
        return (
            0 <= x < len(self.maze.grid[0])
            and 0 <= y < len(self.maze.grid)
            and self.maze.grid[y][x] != 1
        )

    def pathfind(self, goal):
        start = (self.character.x, self.character.y)
        queue = deque([start])
        visited = {start}
        origin = {start: None}

        while queue:
            x, y = queue.popleft()

            if (x, y) == goal:
                step = (x, y)

                while origin[step] != start:
                    step = origin[step]

                dx, dy = step[0] - start[0], step[1] - start[1]
                self.direction = (dx, dy)
                return

            for dx, dy in self.directions:
                nx, ny = x + dx, y + dy

                if self.walkable(nx, ny) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    origin[(nx, ny)] = (x, y)
                    queue.append((nx, ny))
