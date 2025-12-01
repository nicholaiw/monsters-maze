class Canvas:
    def __init__(self, size):
        self.size = size

    def clear(self):
        print("\033[2J\033[H", end="")

    def draw(self, maze, gameObjects, target):
        lines = []
        for y in range(self.size):
            row = []
            for x in range(self.size):
                cameraX, cameraY = self.camera(x, y, target, maze)
                symbol = self.getSymbol(cameraX, cameraY, maze, gameObjects)
                row.append(f" {symbol} ")
            lines.append("".join(row))
        print("\n".join(lines))

    def camera(self, x, y, target, maze):
        offsetX = max(0, min(target.x - self.size // 2, maze.size - self.size))
        offsetY = max(0, min(target.y - self.size // 2, maze.size - self.size))
        return x + offsetX, y + offsetY

    def getSymbol(self, x, y, maze, gameObjects):
        for obj in gameObjects:
            if (obj.x, obj.y) == (x, y):
                return obj.symbol

        if maze.grid[y][x] == 1:
            return "#"
        else:
            return "."
