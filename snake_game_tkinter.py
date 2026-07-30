import tkinter as tk
import random
from enum import Enum
from typing import List, Tuple

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.resizable(True, True)
        
        # Game settings
        self.GRID_SIZE = 20
        self.CANVAS_WIDTH = 800
        self.CANVAS_HEIGHT = 600
        self.GRID_WIDTH = self.CANVAS_WIDTH // self.GRID_SIZE
        self.GRID_HEIGHT = self.CANVAS_HEIGHT // self.GRID_SIZE
        self.SPEED = 100  # milliseconds
        
        # Colors
        self.BG_COLOR = "#000000"
        self.SNAKE_HEAD_COLOR = "#22B14C"
        self.SNAKE_BODY_COLOR = "#006400"
        self.FOOD_COLOR = "#DC143C"
        self.GRID_COLOR = "#333333"
        
        # Create canvas
        self.canvas = tk.Canvas(
            root,
            width=self.CANVAS_WIDTH,
            height=self.CANVAS_HEIGHT,
            bg=self.BG_COLOR,
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Create info frame
        info_frame = tk.Frame(root, bg="#1a1a1a", height=50)
        info_frame.pack(fill=tk.X)
        
        self.score_label = tk.Label(
            info_frame,
            text="Score: 0",
            font=("Arial", 16, "bold"),
            bg="#1a1a1a",
            fg="white"
        )
        self.score_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.status_label = tk.Label(
            info_frame,
            text="Arrow Keys: Move | SPACE: Pause | R: Restart",
            font=("Arial", 10),
            bg="#1a1a1a",
            fg="#CCCCCC"
        )
        self.status_label.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Game state
        self.reset_game()
        self.paused = False
        self.game_over = False
        
        # Bind keys
        self.root.bind("<Up>", lambda e: self.change_direction(Direction.UP))
        self.root.bind("<Down>", lambda e: self.change_direction(Direction.DOWN))
        self.root.bind("<Left>", lambda e: self.change_direction(Direction.LEFT))
        self.root.bind("<Right>", lambda e: self.change_direction(Direction.RIGHT))
        self.root.bind("<space>", lambda e: self.toggle_pause())
        self.root.bind("r", lambda e: self.reset_game())
        self.root.bind("R", lambda e: self.reset_game())
        
        # Start game loop
        self.update_game()
    
    def reset_game(self):
        """Reset game state"""
        self.snake = [
            (self.GRID_WIDTH // 2, self.GRID_HEIGHT // 2),
            (self.GRID_WIDTH // 2 - 1, self.GRID_HEIGHT // 2),
            (self.GRID_WIDTH // 2 - 2, self.GRID_HEIGHT // 2)
        ]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.paused = False
        self.update_labels()
        self.draw()
    
    def generate_food(self) -> Tuple[int, int]:
        """Generate food at random location not on snake"""
        while True:
            x = random.randint(0, self.GRID_WIDTH - 1)
            y = random.randint(0, self.GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                return (x, y)
    
    def change_direction(self, direction: Direction):
        """Change snake direction (prevent reversing)"""
        if self.game_over or self.paused:
            return
        
        opposite = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        
        if direction != opposite[self.direction]:
            self.next_direction = direction
    
    def toggle_pause(self):
        """Pause/resume game"""
        if not self.game_over:
            self.paused = not self.paused
            self.update_labels()
    
    def update_game(self):
        """Update game state"""
        if not self.game_over and not self.paused:
            # Update direction
            self.direction = self.next_direction
            
            # Calculate new head position
            head_x, head_y = self.snake[0]
            dx, dy = self.direction.value
            new_head = (
                (head_x + dx) % self.GRID_WIDTH,
                (head_y + dy) % self.GRID_HEIGHT
            )
            
            # Check self collision
            if new_head in self.snake:
                self.game_over = True
                self.update_labels()
                self.draw()
                return
            
            # Add new head
            self.snake.insert(0, new_head)
            
            # Check food collision
            if new_head == self.food:
                self.score += 10
                self.food = self.generate_food()
            else:
                self.snake.pop()
            
            self.update_labels()
        
        self.draw()
        self.root.after(self.SPEED, self.update_game)
    
    def draw(self):
        """Draw game elements"""
        self.canvas.delete("all")
        
        # Draw grid
        for x in range(0, self.CANVAS_WIDTH, self.GRID_SIZE):
            self.canvas.create_line(x, 0, x, self.CANVAS_HEIGHT, fill=self.GRID_COLOR)
        for y in range(0, self.CANVAS_HEIGHT, self.GRID_SIZE):
            self.canvas.create_line(0, y, self.CANVAS_WIDTH, y, fill=self.GRID_COLOR)
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            rect_x = x * self.GRID_SIZE + 1
            rect_y = y * self.GRID_SIZE + 1
            rect_size = self.GRID_SIZE - 2
            
            if i == 0:  # Head
                self.canvas.create_rectangle(
                    rect_x, rect_y,
                    rect_x + rect_size, rect_y + rect_size,
                    fill=self.SNAKE_HEAD_COLOR,
                    outline="white"
                )
            else:  # Body
                self.canvas.create_rectangle(
                    rect_x, rect_y,
                    rect_x + rect_size, rect_y + rect_size,
                    fill=self.SNAKE_BODY_COLOR,
                    outline="#555555"
                )
        
        # Draw food
        fx = self.food[0] * self.GRID_SIZE + 1
        fy = self.food[1] * self.GRID_SIZE + 1
        food_size = self.GRID_SIZE - 2
        self.canvas.create_oval(
            fx, fy,
            fx + food_size, fy + food_size,
            fill=self.FOOD_COLOR,
            outline="yellow"
        )
        
        # Draw game over message
        if self.game_over:
            self.canvas.create_text(
                self.CANVAS_WIDTH // 2,
                self.CANVAS_HEIGHT // 2 - 30,
                text="GAME OVER",
                font=("Arial", 48, "bold"),
                fill="red"
            )
            self.canvas.create_text(
                self.CANVAS_WIDTH // 2,
                self.CANVAS_HEIGHT // 2 + 30,
                text="Press R to Restart",
                font=("Arial", 24),
                fill="white"
            )
        elif self.paused:
            self.canvas.create_text(
                self.CANVAS_WIDTH // 2,
                self.CANVAS_HEIGHT // 2,
                text="PAUSED",
                font=("Arial", 48, "bold"),
                fill="yellow"
            )
    
    def update_labels(self):
        """Update status labels"""
        self.score_label.config(text=f"Score: {self.score}")
        
        if self.game_over:
            self.status_label.config(text="Game Over! Press R to Restart", fg="#FF6666")
        elif self.paused:
            self.status_label.config(text="PAUSED - Press SPACE to Resume", fg="#FFFF99")
        else:
            self.status_label.config(text="Arrow Keys: Move | SPACE: Pause | R: Restart", fg="#CCCCCC")

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
