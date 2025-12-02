import time
from pynput import keyboard
from gameObject import GameObject, Character
from controller import KeyboardController, AiController, cleanup as cleanupControllers
from maze import Maze
from canvas import Canvas
from constant import Symbols, GameConfig


class Game:
    def __init__(
        self,
        mazeSize=GameConfig.MAZE_SIZE,
        viewportSize=GameConfig.VIEWPORT_SIZE,
        tickRate=GameConfig.TICK_RATE,
    ):
        self.running = True
        self.maze = Maze(mazeSize)
        self.canvas = Canvas(viewportSize)
        self.gameObjects = []
        self.tickRate = tickRate

    def spawnGameObject(self, objectClass, symbol, **kwargs):
        x, y = self.maze.getEmptyTile()
        obj = objectClass(x, y, symbol=symbol, **kwargs)
        self.gameObjects.append(obj)
        return obj

    def start(self):
        self.spawnGameObject(
            Character,
            Symbols.HUMAN,
            role="human",
            controller=KeyboardController(
                {
                    keyboard.Key.left: (-1, 0),
                    keyboard.Key.right: (1, 0),
                    keyboard.Key.up: (0, -1),
                    keyboard.Key.down: (0, 1),
                }
            ),
        )

        self.spawnGameObject(
            Character,
            Symbols.HUMAN,
            role="human",
            controller=KeyboardController(
                {
                    keyboard.KeyCode.from_char("a"): (-1, 0),
                    keyboard.KeyCode.from_char("d"): (1, 0),
                    keyboard.KeyCode.from_char("w"): (0, -1),
                    keyboard.KeyCode.from_char("s"): (0, 1),
                }
            ),
        )

        self.spawnGameObject(
            Character,
            Symbols.MONSTER,
            role="monster",
            controller=KeyboardController(
                {
                    keyboard.KeyCode.from_char("j"): (-1, 0),
                    keyboard.KeyCode.from_char("l"): (1, 0),
                    keyboard.KeyCode.from_char("i"): (0, -1),
                    keyboard.KeyCode.from_char("k"): (0, 1),
                }
            ),
        )

        self.spawnGameObject(
            Character,
            Symbols.MONSTER,
            role="monster",
            controller=AiController(GameConfig.MONSTER_VIEW_RANGE),
        )

    def run(self):
        try:
            self.start()
            while self.running:
                self.update()
                self.draw()
                time.sleep(self.tickRate)
        finally:
            self.cleanup()

    def update(self):
        for obj in self.gameObjects:
            obj.update(self)

    def draw(self):
        self.canvas.clear()

        players = [
            obj
            for obj in self.gameObjects
            if hasattr(obj, "controller")
            and not isinstance(obj.controller, AiController)
        ]

        for character in players:
            self.canvas.draw(self.maze, self.gameObjects, character)
            print()

    def cleanup(self):
        cleanupControllers()


if __name__ == "__main__":
    game = Game()
    game.run()
