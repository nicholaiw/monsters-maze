import time
from pynput import keyboard
from gameObject import Character
from controller import KeyboardController, AiMonster
from maze import Maze
from canvas import Canvas


class Game:
    def __init__(self):
        self.running = True
        self.maze = Maze(15)
        self.canvas = Canvas(15)
        self.gameObjects = []

        self.player = self.spawnGameObject(Character, "@", role="human")
        self.playerController = KeyboardController(
            {
                keyboard.Key.left: (-1, 0),
                keyboard.Key.right: (1, 0),
                keyboard.Key.up: (0, -1),
                keyboard.Key.down: (0, 1),
            }
        )

        self.monster = self.spawnGameObject(Character, "&", role="monster")
        self.monsterController = AiMonster(self.monster, 5, self.maze, self.gameObjects)

    def spawnGameObject(self, objClass, symbol, **kwargs):
        x, y = self.maze.getEmptyTile()
        obj = objClass(x, y, symbol=symbol, **kwargs)
        self.gameObjects.append(obj)
        return obj

    def run(self):
        while self.running:
            self.update()
            self.draw()
            time.sleep(0.25)

    def update(self):
        self.monster.move(self.monsterController.getDirection(), self.maze.grid)
        self.player.move(self.playerController.getDirection(), self.maze.grid)

        if self.monster.x == self.player.x and self.monster.y == self.player.y:
            quit()

    def draw(self):
        self.canvas.clear()
        self.canvas.draw(self.maze, self.gameObjects, self.player)


game = Game()
game.run()
