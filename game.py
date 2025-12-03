import pygame
from entity import Entity, Character, Door
from controller import PlayerController, AiController
from maze import Maze
from canvas import Canvas
from config import Settings


class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()
        self.maze = Maze(Settings.MAZE_SIZE)
        self.canvas = Canvas(Settings.WINDOW_SIZE, Settings.VIEW_PORT_SIZE)
        self.entities = []
        self.player = None

    def _spawnEntity(self, entityClass, **kwargs):
        x, y = self.maze.getEmptyTile()
        obj = entityClass(x, y, **kwargs)
        self.entities.append(obj)
        return obj

    def setup(self):
        self._spawnEntity(Door)

        self.player = self._spawnEntity(
            Character,
            role="human",
            controller=PlayerController(
                {
                    pygame.K_UP: (0, -1),
                    pygame.K_DOWN: (0, 1),
                    pygame.K_LEFT: (-1, 0),
                    pygame.K_RIGHT: (1, 0),
                }
            ),
            moveDelay=15,
        )

        for i in range(Settings.MONSTER_AMOUNT):
            self._spawnEntity(
                Character,
                role="monster",
                controller=AiController(),
                moveDelay=15,
            )

    def _checkEscape(self):
        door = next((obj for obj in self.entities if isinstance(obj, Door)), None)
        if self.player.x == door.x and self.player.y == door.y:
            self.running = False

    def _checkCaught(self):
        for entity in self.entities:
            if isinstance(entity, Character) and entity.role == "monster":
                if entity.x == self.player.x and entity.y == self.player.y:
                    self.running = False

    def update(self):
        for entity in self.entities:
            entity.update(self.maze)

        self._checkEscape()
        self._checkCaught()

    def draw(self):
        self.canvas.draw(self.player, self.maze, self.entities)
        pygame.display.update()

    def run(self):
        self.setup()

        while self.running:
            pygame.event.pump()

            self.update()
            self.draw()

            self.clock.tick(Settings.TICK_RATE)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
