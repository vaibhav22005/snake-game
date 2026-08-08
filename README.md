# Snake Game

A classic Snake game built with Python and Pygame featuring a clean GUI and smooth gameplay.

## Features

- **Classic Gameplay**: Navigate the snake to eat food and grow longer
- **Smooth Controls**: Responsive keyboard controls with direction buffering
- **Score Tracking**: Real-time score display
- **Visual Design**: Grid background, distinct snake head, colored segments, and food
- **Pause Feature**: Press SPACE to pause/resume the game
- **Game Over Screen**: Shows final score with restart option
- **Collision Detection**: Game ends on self-collision

## Requirements

- Python 3.7+
- Pygame

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Play

Run the game:
```bash
python snake_game.py
```

### Controls

- **Arrow Keys**: Move the snake (UP, DOWN, LEFT, RIGHT)
- **SPACE**: Pause/Resume or Restart the game
- **ESC**: Exit the game

### Game Mechanics

- Eat the red/yellow food to grow and earn 10 points
- Avoid colliding with yourself
- The snake wraps around the edges of the screen
- Each food eaten makes the game slightly faster

## Game Elements

- **Green Snake Head**: Your snake's front
- **Dark Green Segments**: Snake body
- **Red/Yellow Food**: Collect to grow and score points
- **Grid Background**: Visual reference for snake movement

## Tips

- Plan ahead to avoid trapping yourself
- Use the pause feature to think about your next move
- The game gets progressively harder as you grow longer

Enjoy the game!
