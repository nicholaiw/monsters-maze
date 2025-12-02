from constant import Symbols, TileType


class Canvas:
    def __init__(self, viewportSize):
        self.viewportSize = viewportSize

    def clear(self):
        print("\033[2J\033[H", end="")

    def draw(self, maze, gameObjects, target):
        lines = []

        for y in range(self.viewportSize):
            row = []
            for x in range(self.viewportSize):
                worldX, worldY = self._getWorldPosition(x, y, target, maze)
                symbol = self._getSymbolAt(worldX, worldY, maze, gameObjects)
                row.append(f" {symbol} ")
            lines.append("".join(row))

        print("\n".join(lines))

    def _getWorldPosition(self, viewX, viewY, target, maze):
        halfView = self.viewportSize // 2

        offsetX = max(0, min(target.x - halfView, maze.size - self.viewportSize))
        offsetY = max(0, min(target.y - halfView, maze.size - self.viewportSize))

        return viewX + offsetX, viewY + offsetY

    def _getSymbolAt(self, x, y, maze, gameObjects):
        for obj in gameObjects:
            if obj.x == x and obj.y == y:
                return obj.symbol

        if not (0 <= x < maze.size and 0 <= y < maze.size):
            return Symbols.WALL

        if maze.grid[y][x] == TileType.WALL:
            return Symbols.WALL
        else:
            return Symbols.FLOOR
