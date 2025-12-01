from collections import deque
from pynput import keyboard


class KeyboardController:
    def __init__(self, bindings):
        self.bindings = bindings
        self.direction = None
        self.listener = keyboard.Listener(on_release=self.getKey)
        self.listener.start()

    def getKey(self, key):
        self.direction = self.bindings.get(key, self.direction)

    def getDirection(self):
        return self.direction


class AiController:
    def __init__(self, character, view, maze, gameObjects):
        self.character = character
        self.view = view
        self.maze = maze
        self.gameObjects = gameObjects
        self.direction = None

    def getDirection(self):
        target = None
        for obj in self.gameObjects:
            if hasattr(obj, "role") and obj.role == "human":
                if (
                    abs(obj.x - self.character.x) + abs(obj.y - self.character.y)
                    <= self.view
                ):
                    target = obj
                    break

        if target:
            movement = self.pathfind(
                self.maze, (self.character.x, self.character.y), (target.x, target.y)
            )
            if movement:
                dx, dy = movement[0] - self.character.x, movement[1] - self.character.y
                self.direction = {
                    (1, 0): "right",
                    (-1, 0): "left",
                    (0, -1): "up",
                    (0, 1): "down",
                }.get((dx, dy), None)

        return self.direction

    def pathfind(self, maze, start, goal):
        queue = deque([start])
        visited = set([start])
        origin = {start: None}

        while queue:
            x, y = queue.popleft()

            if (x, y) == goal:
                step = (x, y)
                while origin[step] != start:
                    step = origin[step]
                return step

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < len(maze.grid[0])
                    and 0 <= ny < len(maze.grid)
                    and maze.grid[ny][nx] != 1
                    and (nx, ny) not in visited
                ):
                    queue.append((nx, ny))
                    visited.add((nx, ny))
                    origin[(nx, ny)] = (x, y)

        return None
