import random
from collections import deque
import pygame
from config import TileType


class PlayerController:
    def __init__(self, bindings):
        self.bindings = bindings

    def getDirection(self, character, maze):
        keys = pygame.key.get_pressed()

        for key, direction in self.bindings.items():
            if keys[key]:
                return direction


class AiController:

    def __init__(self):
        self.visited = {}
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    def getDirection(self, character, maze):

        position = (character.x, character.y)

        self.visited[position] = self.visited.get(position, 0) + 1
        goal = self._leastVisited(character, maze)
        return self._pathfind(character, goal, maze)

    def _leastVisited(self, character, maze):
        random.shuffle(self.directions) 

        tiles = []
        for dx, dy in self.directions:
            nx, ny = character.x + dx, character.y + dy
            if self._isWalkable(nx, ny, maze):
                visits = self.visited.get((nx, ny), 0)
                tiles.append(((nx, ny), visits))

        return min(tiles, key=lambda t: t[1])[0]

    def _isWalkable(self, x, y, maze):
        return (
            0 <= x < maze.size
            and 0 <= y < maze.size
            and maze.grid[y][x] == TileType.FLOOR
        )

    def _pathfind(self, character, goal, maze):
        start = (character.x, character.y)
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

            for dx, dy in self.directions:
                nx, ny = current[0] + dx, current[1] + dy
                neighbor = (nx, ny)
                if self._isWalkable(nx, ny, maze) and neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)
