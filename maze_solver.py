# maze_solver.py

from collections import deque
import time

class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.start = None
        self.end = None
        self.came_from = {}
        self.visited = set()
        self.path = []

    def set_start_end(self, start, end):
        self.start = start
        self.end = end

    def solve_bfs(self, animate_callback=None, animation_speed=0.05):
        if not self.start or not self.end:
            raise ValueError("Start and end points must be set before solving.")

        queue = deque([self.start])
        self.came_from = {self.start: None}
        self.visited = set([self.start])

        while queue:
            current = queue.popleft()

            if current == self.end:
                self._construct_path()
                return self.path

            for neighbor in self.get_neighbors(current):
                if neighbor not in self.visited:
                    queue.append(neighbor)
                    self.visited.add(neighbor)
                    self.came_from[neighbor] = current
                    if animate_callback:
                        animate_callback(neighbor)
                        time.sleep(animation_speed)

        return None  # No path found

    def _construct_path(self):
        self.path = []
        current = self.end
        while current != self.start:
            self.path.append(current)
            current = self.came_from.get(current)
            if current is None:
                break
        self.path.append(self.start)
        self.path.reverse()

    def get_neighbors(self, position):
        x, y = position
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.maze.height and 0 <= ny < self.maze.width and self.maze.grid[nx][ny] == 0:
                neighbors.append((nx, ny))
        return neighbors
