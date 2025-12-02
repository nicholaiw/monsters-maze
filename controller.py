import random
from collections import deque
from pynput import keyboard
from constant import TileType


class ControllerManager:
    def __init__(self):
        self.controllers = []
        self.listener = None

    def register(self, controller):
        self.controllers.append(controller)
        if self.listener is None:
            self.listener = keyboard.Listener(on_press=self._onPress)
            self.listener.start()

    def _onPress(self, key):
        for controller in self.controllers:
            if hasattr(controller, "onPress"):
                controller.onPress(key)

    def cleanup(self):
        if self.listener:
            self.listener.stop()
            self.listener = None


_manager = ControllerManager()


class Controller:
    def getDirection(self, character, gameObjects, maze):
        raise NotImplementedError


class KeyboardController(Controller):
    def __init__(self, bindings):
        self.bindings = bindings
        self.direction = None
        _manager.register(self)

    def onPress(self, key):
        if key in self.bindings:
            self.direction = self.bindings[key]

    def getDirection(self, character, gameObjects, maze):
        direction = self.direction
        self.direction = None
        return direction


class AiController(Controller):

    DIRECTIONS = [(1, 0), (-1, 0), (0, -1), (0, 1)]

    def __init__(self, viewRange):
        self.viewRange = viewRange
        self.visited = {}
        self.target = None

    def getDirection(self, character, gameObjects, maze):
        self._updateVisited(character)
        self._findVisibleTarget(character, gameObjects)

        if self.target and (character.x, character.y) == (self.target.x, self.target.y):
            self.target = None

        if self.target:
            goal = (self.target.x, self.target.y)
        else:
            goal = self._getLeastVisitedTile(character, maze)

        return self._pathfind(character, goal, maze)

    def _findVisibleTarget(self, character, gameObjects):
        for obj in gameObjects:
            if getattr(obj, "role", None) == "human":
                distance = abs(obj.x - character.x) + abs(obj.y - character.y)
                if distance <= self.viewRange:
                    self.target = obj
                    return

    def _updateVisited(self, character):
        position = (character.x, character.y)
        self.visited[position] = self.visited.get(position, 0) + 1

    def _getLeastVisitedTile(self, character, maze):
        tiles = []
        for dx, dy in self.DIRECTIONS:
            nx, ny = character.x + dx, character.y + dy
            if self._isWalkable(nx, ny, maze):
                visits = self.visited.get((nx, ny), 0)
                tiles.append(((nx, ny), visits))

        if not tiles:
            return (character.x, character.y)

        minVisits = min(tile[1] for tile in tiles)
        leastVisited = [tile[0] for tile in tiles if tile[1] == minVisits]
        return random.choice(leastVisited)

    def _isWalkable(self, x, y, maze):
        return (
            0 <= x < maze.size
            and 0 <= y < maze.size
            and maze.grid[y][x] == TileType.FLOOR
        )

    def _pathfind(self, character, goal, maze):
        start = (character.x, character.y)

        if start == goal:
            return None

        queue = deque([start])
        visited = {start}
        parent = {start: None}

        while queue:
            current = queue.popleft()

            if current == goal:
                step = current
                while parent[step] != start:
                    step = parent[step]

                dx = step[0] - start[0]
                dy = step[1] - start[1]
                return (dx, dy)

            for dx, dy in self.DIRECTIONS:
                nx, ny = current[0] + dx, current[1] + dy
                neighbor = (nx, ny)

                if self._isWalkable(nx, ny, maze) and neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

        return None


def cleanup():
    _manager.cleanup()
