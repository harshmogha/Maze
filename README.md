# Maze Solver

This project is a graphical maze generator and solver implemented using Python and Tkinter. It allows users to generate random mazes, upload mazes from image files, and solve them using the Breadth-First Search (BFS) algorithm. The GUI provides an interactive and visually appealing way to explore maze-solving algorithms.

## Features

- **Maze Generation**:
  - **Recursive Backtracking**: Generates a perfect maze with one unique solution.
  - **Random Maze**: Generates a random maze with a guaranteed path from start to finish.
  
- **Maze Solving**:
  - **BFS Algorithm**: Uses Breadth-First Search to find the shortest path from the start to the end of the maze.

- **3D Effect**:
  - The maze walls and paths are rendered with a 3D effect, enhancing the visual appeal of the maze.

- **Maze Upload**:
  - Upload a maze from an image file. The image is converted into a binary grid, and the maze is resized to fit a 20x20 grid.

- **Interactive GUI**:
  - Users can interact with the GUI to generate new mazes, solve them, and control the speed of the solving animation.

## Requirements

- Python 3.x
- Tkinter
- Pillow (PIL)
- NumPy

You can install the required libraries using pip:

```bash
pip install pillow numpy
```

## How to Run

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/maze-solver.git
   cd maze-solver
   ```

2. **Run the Maze Solver**:
   ```bash
   python maze_solver.py
   ```

3. **Interact with the GUI**:
   - Click "Generate New Maze" to generate a random maze.
   - Click "Solve with BFS" to find the path from start to end.
   - Use the "Upload Maze" button to load a maze from an image file.
   - Adjust the "Animation Speed" slider to control the speed of the BFS animation.

## File Structure

- `maze_solver.py`: The main file containing the GUI and maze-solving logic.
- `README.md`: Project description and instructions (this file).

## Maze Generation Methods

- **Recursive Backtracking**:
  - A classic algorithm that creates a perfect maze (one solution only) by carving out paths in a grid.
  
- **Random Maze**:
  - A more chaotic maze generation technique that guarantees a path from start to finish but might have multiple solutions.

## Maze Solver

- The BFS algorithm ensures the shortest path from the start to the end of the maze.
- The solver visualizes the exploration of the maze, providing a clear view of the algorithm's behavior.

## Maze Upload

- Convert an image to a maze by uploading an image file. The image is processed and resized to fit a 20x20 grid.

## Future Enhancements

- Implement additional algorithms like A* or DFS for maze solving.
- Add support for larger maze sizes.
- Improve the 3D rendering for more realistic visuals.
- Add an option to save the generated maze as an image file.

## License

This project is open-source and available under the [MIT License](LICENSE).
