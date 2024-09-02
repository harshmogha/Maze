# maze_gui.py

import tkinter as tk
from tkinter import ttk, filedialog
import random
from PIL import Image, ImageTk
import time

from maze_generator import Maze
from maze_solver import MazeSolver

class MazeSolverGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Maze Solver")
        self.master.geometry("800x750")
        self.master.configure(bg="#f0f0f0")
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.frame = ttk.Frame(master, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.frame, width=600, height=600, bg="#D2B48C", highlightthickness=0)
        self.canvas.pack(pady=20)

        self.grid_size = 30
        self.maze = None
        self.start = None
        self.end = None
        self.solver = None

        self.button_frame = ttk.Frame(self.frame)
        self.button_frame.pack(pady=10)

        self.solve_button = ttk.Button(self.button_frame, text="Solve with BFS", command=self.solve_maze, style="TButton")
        self.solve_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = ttk.Button(self.button_frame, text="Generate New Maze", command=self.generate_new_maze, style="TButton")
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.upload_button = ttk.Button(self.button_frame, text="Upload Maze", command=self.upload_maze, style="TButton")
        self.upload_button.pack(side=tk.LEFT, padx=5)

        self.style.configure("TButton", padding=10, font=("Arial", 12))

        self.status_label = tk.Label(self.frame, text="", font=("Arial", 12), bg="#f0f0f0")
        self.status_label.pack(pady=10)

        self.speed_scale = ttk.Scale(self.frame, from_=1, to=100, orient=tk.HORIZONTAL, length=200)
        self.speed_scale.set(50)
        self.speed_scale.pack(pady=10)

        self.speed_label = tk.Label(self.frame, text="Animation Speed", font=("Arial", 10), bg="#f0f0f0")
        self.speed_label.pack()

        self.generate_new_maze()

    def draw_maze(self):
        self.canvas.delete("all")
        for x in range(self.maze.height):
            for y in range(self.maze.width):
                if self.maze.grid[x][y] == 1:  # Wall
                    self.draw_3d_wall(x, y)
                else:  # Path
                    self.draw_3d_path(x, y)
        
        self.draw_point(self.start, "#2ECC71", "#27AE60", "Start")
        self.draw_point(self.end, "#E74C3C", "#C0392B", "End")

    def draw_3d_wall(self, x, y):
        # Main wall face
        self.canvas.create_rectangle(
            y * self.grid_size,
            x * self.grid_size,
            (y + 1) * self.grid_size,
            (x + 1) * self.grid_size,
            fill="#8B4513",
            outline="#5D2E0C",
            width=1
        )
        # Top edge
        self.canvas.create_polygon(
            y * self.grid_size, x * self.grid_size,
            (y + 1) * self.grid_size, x * self.grid_size,
            (y + 0.85) * self.grid_size, (x + 0.15) * self.grid_size,
            (y + 0.15) * self.grid_size, (x + 0.15) * self.grid_size,
            fill="#A0522D",
            outline="#5D2E0C",
            width=1
        )
        # Right edge
        self.canvas.create_polygon(
            (y + 1) * self.grid_size, x * self.grid_size,
            (y + 1) * self.grid_size, (x + 1) * self.grid_size,
            (y + 0.85) * self.grid_size, (x + 0.85) * self.grid_size,
            (y + 0.85) * self.grid_size, (x + 0.15) * self.grid_size,
            fill="#6B3E26",
            outline="#5D2E0C",
            width=1
        )

    def draw_3d_path(self, x, y):
        # Main path face
        self.canvas.create_rectangle(
            y * self.grid_size,
            x * self.grid_size,
            (y + 1) * self.grid_size,
            (x + 1) * self.grid_size,
            fill="#F4A460",
            outline="#D2691E",
            width=1
        )
        # Top edge
        self.canvas.create_polygon(
            y * self.grid_size, x * self.grid_size,
            (y + 1) * self.grid_size, x * self.grid_size,
            (y + 0.92) * self.grid_size, (x + 0.08) * self.grid_size,
            (y + 0.08) * self.grid_size, (x + 0.08) * self.grid_size,
            fill="#DEB887",
            outline="#D2691E",
            width=1
        )
        # Right edge
        self.canvas.create_polygon(
            (y + 1) * self.grid_size, x * self.grid_size,
            (y + 1) * self.grid_size, (x + 1) * self.grid_size,
            (y + 0.92) * self.grid_size, (x + 0.92) * self.grid_size,
            (y + 0.92) * self.grid_size, (x + 0.08) * self.grid_size,
            fill="#CD853F",
            outline="#D2691E",
            width=1
        )

    def draw_point(self, point, fill_color, outline_color, label):
        x, y = point
        self.canvas.create_rectangle(
            y * self.grid_size + 2,
            x * self.grid_size + 2,
            (y + 1) * self.grid_size - 2,
            (x + 1) * self.grid_size - 2,
            fill=fill_color,
            outline=outline_color,
            width=2
        )
        self.canvas.create_text(
            (y + 0.5) * self.grid_size,
            (x + 0.5) * self.grid_size,
            text=label,
            fill="white",
            font=("Arial", 10, "bold")
        )

    def solve_maze(self):
        self.canvas.delete("visited")
        self.canvas.delete("path")
        self.status_label.config(text="Solving maze...", fg="blue")
        self.master.update()

        self.solver = MazeSolver(self.maze)
        self.solver.set_start_end(self.start, self.end)
        animation_speed = 0.1 - (self.speed_scale.get() / 100) * 0.099

        path = self.solver.solve_bfs(animate_callback=self.animate_visit, animation_speed=animation_speed)

        if path:
            self.animate_path(path)
            self.status_label.config(text=f"Path found! Length: {len(path)}", fg="green")
        else:
            self.status_label.config(text="No path found for this maze.", fg="red")

    def animate_visit(self, cell):
        x, y = cell
        self.canvas.create_rectangle(
            y * self.grid_size + 5,
            x * self.grid_size + 5,
            (y + 1) * self.grid_size - 5,
            (x + 1) * self.grid_size - 5,
            fill="white",
            outline="",
            tags="visited"
        )
        self.master.update()

    def animate_path(self, path):
        for i, cell in enumerate(path):
            x, y = cell
            color = self.get_gradient_color(i, len(path))
            self.canvas.create_rectangle(
                y * self.grid_size + 5,
                x * self.grid_size + 5,
                (y + 1) * self.grid_size - 5,
                (x + 1) * self.grid_size - 5,
                fill=color,
                outline="",
                tags="path"
            )
            self.master.update()
            time.sleep(0.05 - (self.speed_scale.get() / 100) * 0.049)

    def get_gradient_color(self, index, total):
        r = int(41 + (231 - 41) * (total - index) / total)
        g = int(128 + (76 - 128) * (total - index) / total)
        b = int(185 + (60 - 185) * (total - index) / total)
        return f'#{r:02x}{g:02x}{b:02x}'

    def generate_new_maze(self):
        self.maze = Maze(20, 20)
        if random.choice([True, False]):
            self.maze.generate_maze()  
        else:
            self.maze.generate_random_maze() 
        
        empty_cells = [(x, y) for x in range(self.maze.height) for y in range(self.maze.width) if self.maze.grid[x][y] == 0]
        if len(empty_cells) < 2:
            self.status_label.config(text="Failed to generate a valid maze. Try again.", fg="red")
            return
        
        self.start, self.end = random.sample(empty_cells, 2)
        
        self.draw_maze()
        self.status_label.config(text="New maze generated. Click 'Solve with BFS' to find the path", fg="black")

    def upload_maze(self):
        filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if filename:
            self.maze = Maze(20, 20)  # Create a 20x20 maze
            self.maze.load_from_image(filename)
            
            empty_cells = [(x, y) for x in range(self.maze.height) for y in range(self.maze.width) if self.maze.grid[x][y] == 0]
            if len(empty_cells) < 2:
                self.status_label.config(text="Invalid maze: Not enough empty cells", fg="red")
                return
            
            self.start, self.end = random.sample(empty_cells, 2)
            
            self.grid_size = min(600 // max(self.maze.width, self.maze.height), 30)
            self.canvas.config(width=self.maze.width * self.grid_size, height=self.maze.height * self.grid_size)
            
            self.draw_maze()
            self.status_label.config(text="Maze uploaded. Click 'Solve with BFS' to find the path", fg="black")
