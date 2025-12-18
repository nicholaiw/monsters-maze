# Monsters Maze

## Purpose

This is a learning project where i experiment with:
- **Maze generation** - Recursive backtracking algorithm
- **Pathfinding** - BFS implementation
- **AI behavior** - Visit-based exploration strategy


## File content

- `maze.py` - Recursive backtracking maze generator
- `controller.py` - BFS pathfinding for AI entities with visit tracking, input handling for player controlled entities
- `game.py` - Main game loop
- `entity.py` - Entity base classes (characters, doors)
- `canvas.py` - Pygame rendering
- `config.py` - Game settings and tile types


## How It Works

The game creates a maze where:
- Player navigates to reach a door (goal)
- AI monsters use BFS to pathfind toward least-visited tiles
- Monsters track visited tiles to encourage exploration

## Dependencies

- Python3
- Pygame

## How to run
```bash
python game.py
```

## Play it online

[itch.io](https://nicholaiw.itch.io/monsters-maze)