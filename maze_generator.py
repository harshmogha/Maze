# maze_generator.py

import random
import numpy as np
from PIL import Image

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[1 for _ in range(width)] for _ in range(height)] 
        self.generate_maze()

    def generate_maze(self):
        self._recursive_backtracking(0, 0)
        self.grid[0][0] = 0
        self.grid[self.width-1][self.height-1] = 0

    def _recursive_backtracking(self, x, y):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + 2 * dx, y + 2 * dy

            if 0 <= nx < self.width and 0 <= ny < self.height and self.grid[nx][ny] == 1:
                self.grid[x + dx][y + dy] = 0
                self.grid[nx][ny] = 0
                self._recursive_backtracking(nx, ny)

    def generate_random_maze(self):
        for x in range(self.width):
            for y in range(self.height):
                self.grid[x][y] = random.choice([0, 1])
        
        self.grid[0][0] = 0
        self.grid[self.width-1][self.height-1] = 0

        self.create_path()

    def create_path(self):
        x, y = 0, 0
        path = [(x, y)]
        while (x, y) != (self.width - 1, self.height - 1):
            self.grid[x][y] = 0
            direction = random.choice(["down", "right"])
            if direction == "down" and x < self.width - 1:
                x += 1
            elif direction == "right" and y < self.height - 1:
                y += 1
            path.append((x, y))

        for x, y in path:
            self.grid[x][y] = 0

    def load_from_image(self, filename):
        image = Image.open(filename).convert('L')  # Convert to grayscale
        image_array = np.array(image)
        
        # Apply threshold to convert to binary
        threshold = 128
        binary_array = (image_array > threshold).astype(int)
        
        # Invert the binary array so that walls are 1 and paths are 0
        self.grid = 1 - binary_array
        
        self.height, self.width = self.grid.shape
        self.convert_to_program_maze()

    def convert_to_program_maze(self):
        # Resize the maze to 20x20
        new_width, new_height = 20, 20
        resized_grid = np.zeros((new_height, new_width), dtype=int)
        
        for x in range(new_height):
            for y in range(new_width):
                orig_x = int(x * self.height / new_height)
                orig_y = int(y * self.width / new_width)
                resized_grid[x, y] = self.grid[orig_x, orig_y]
        
        self.width, self.height = new_width, new_height
        self.grid = resized_grid.tolist()
        
        # Ensure start and end are open
        self.grid[0][0] = 0
        self.grid[self.height-1][self.width-1] = 0
        
        # Create a path if one doesn't exist
        if not self.path_exists():
            self.create_path()

    def path_exists(self):
        visited = set()
        stack = [(0, 0)]
        
        while stack:
            x, y = stack.pop()
            if (x, y) == (self.height-1, self.width-1):
                return True
            if (x, y) not in visited:
                visited.add((x, y))
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.height and 0 <= ny < self.width and self.grid[nx][ny] == 0:
                        stack.append((nx, ny))
        return False
