import pygame
from config import Colors, TileType
from entity import Door, Character


class Canvas:
    def __init__(self, windowSize, viewportSize):
        self.windowSize = windowSize
        self.viewportSize = viewportSize
        self.tileSize = windowSize // viewportSize
        self.screen = pygame.display.set_mode((windowSize, windowSize))
        pygame.display.set_caption("Monsters Maze")

    def _worldToView(self, wx, wy, target, mazeSize):
        half = self.viewportSize // 2

        sx = (
            wx - max(0, min(target.x - half, mazeSize - self.viewportSize))
        ) * self.tileSize
        sy = (
            wy - max(0, min(target.y - half, mazeSize - self.viewportSize))
        ) * self.tileSize

        return sx, sy

    def _getEntityColor(self, entity):
        if isinstance(entity, Door):
            return Colors.DOOR
        elif isinstance(entity, Character):
            if entity.role == "human":
                return Colors.HUMAN
            elif entity.role == "monster":
                return Colors.MONSTER
        return None

    def _drawTile(self, sx, sy, color):
        pygame.draw.rect(self.screen, color, (sx, sy, self.tileSize, self.tileSize))

    def draw(self, target, maze, entities):
        for wy in range(maze.size):
            for wx in range(maze.size):
                sx, sy = self._worldToView(wx, wy, target, maze.size)

                if 0 <= sx < self.windowSize and 0 <= sy < self.windowSize:
                    tileType = maze.grid[wy][wx]

                    if tileType == TileType.WALL:
                        color = Colors.WALL
                    else:
                        color = Colors.FLOOR

                    self._drawTile(sx, sy, color)

        for entity in entities:
            sx, sy = self._worldToView(entity.x, entity.y, target, maze.size)

            if 0 <= sx < self.windowSize and 0 <= sy < self.windowSize:
                color = self._getEntityColor(entity)

                if color is not None:
                    self._drawTile(sx, sy, color)
