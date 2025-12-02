class Symbols:
    WALL = "#"
    FLOOR = "."
    HUMAN = "@"
    MONSTER = "&"
    DOOR = "+"


class TileType:
    WALL = 1
    FLOOR = 0


class GameConfig:
    MAZE_SIZE = 15
    VIEWPORT_SIZE = 15
    TICK_RATE = 0.25
    MONSTER_VIEW_RANGE = 3
