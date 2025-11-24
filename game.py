import time

from pynput import keyboard

from entity import Character, Wall
from controller import KeyboardController


class Game:
    def __init__(self):
        self.running = True
        self.entities = []
        self.player = Character(x=0, y=0, symbol="@", collision=False, view=5)
        self.playerController = KeyboardController(
            {
                keyboard.Key.left: "left",
                keyboard.Key.right: "right",
                keyboard.Key.up: "up",
                keyboard.Key.down: "down",
            }
        )
        self.entities.append(self.player)
        self.entities.append(Wall(x=1, y=1, symbol="#", collision=True))

    def draw(self, entities, target):
        lines = ["\033[2J\033[H"]

        for y in range(target.view):
            row = []

            for x in range(target.view):
                offsetX = x + (target.x - target.view // 2)
                offsetY = y + (target.y - target.view // 2)

                symbol = "."
                for entity in entities:
                    if entity.x == offsetX and entity.y == offsetY:
                        symbol = entity.symbol
                        break

                row.append(f" {symbol} ")
            lines.append("".join(row))
        print("\n".join(lines))

    def run(self):
        while self.running:
            self.player.move(self.playerController.getDirection(), self.entities)
            self.draw(self.entities, self.player)
            time.sleep(0.5)


game = Game()
game.run()
