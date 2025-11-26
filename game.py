import time

from pynput import keyboard
from controller import KeyboardController
from map import Map


class Game:
    def __init__(self):
        self.running = True
        self.map = Map()
        self.playerController = KeyboardController(
            {
                keyboard.Key.left: "left",
                keyboard.Key.right: "right",
                keyboard.Key.up: "up",
                keyboard.Key.down: "down",
            }
        )

    def draw(self, entities, target):
        lines = ["\033[2J\033[H"]

        
        for y in range(target.view):
            row = []
            for x in range(target.view):
                offsetX = x + max(0, min(target.x - target.view // 2, self.map.size - target.view))
                offsetY = y + max(0, min(target.y - target.view // 2, self.map.size - target.view))

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
            self.map.player.move(
                self.playerController.getDirection(), self.map.entities
            )
            self.draw(self.map.entities, self.map.player)
            time.sleep(0.5)


game = Game()
game.run()
