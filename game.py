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

    def start(self):

        self.spawnGameObject(GameObject, Symbols.DOOR)

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
            Symbols.MONSTER,
            role="monster",
            controller=AiController(GameConfig.MONSTER_VIEW_RANGE),
        )

    def run(self):
        try:
            self.start()
            while self.running:
                self._checkGameOver()
                self.update()
                self.draw()
                time.sleep(self.tickRate)
        finally:
            self.cleanup()

    def update(self):

        for obj in self.gameObjects[:]:
            obj.update(self)

        self._checkKilled()
        self._checkEscape()

    def _checkKilled(self):
        monsters = [
            obj for obj in self.gameObjects if getattr(obj, "role", None) == "monster"
        ]
        humans = [
            obj for obj in self.gameObjects if getattr(obj, "role", None) == "human"
        ]

        for monster in monsters:
            for human in humans[:]:
                if monster.x == human.x and monster.y == human.y:
                    self.gameObjects.remove(human)

    def _checkEscape(self):
        door = next(
            (obj for obj in self.gameObjects if obj.symbol == Symbols.DOOR), None
        )

        if not door:
            return

        humans = [
            obj for obj in self.gameObjects if getattr(obj, "role", None) == "human"
        ]

        for human in humans[:]:
            if human.x == door.x and human.y == door.y:
                self.gameObjects.remove(human)

    def _checkGameOver(self):
        humans = [
            obj for obj in self.gameObjects if getattr(obj, "role", None) == "human"
        ]

        if len(humans) == 0:
            self.running = False

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
