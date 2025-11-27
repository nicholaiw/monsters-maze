import time
from pynput import keyboard
from gameObject import Character, Item
from controller import KeyboardController
from maze import Maze
from canvas import Canvas


class Game:
    def __init__(self):
        self.running = True
        self.maze = Maze(15)
        self.canvas = Canvas(15)
        self.gameObjects = []

        self.player = self.spawnGameObject(Character, "@")
        self.playerController = KeyboardController(
            {
                keyboard.Key.left: "left",
                keyboard.Key.right: "right",
                keyboard.Key.up: "up",
                keyboard.Key.down: "down",
            }
        )

    def spawnGameObject(self, objClass, symbol, **kwargs):
        x, y = self.maze.getEmptyTile()
        obj = objClass(x, y, symbol=symbol, **kwargs)
        self.gameObjects.append(obj)
        return obj

    def run(self):
        while self.running:
            self.update()
            self.draw()
            time.sleep(0.5)

    def update(self):
        self.player.move(self.playerController.getDirection(), self.maze.grid)

    def draw(self):
        self.canvas.clear()
        self.canvas.draw(self.maze, self.gameObjects, self.player)


game = Game()
game.run()
