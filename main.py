# main.py

import tkinter as tk
from maze_gui import MazeSolverGUI

def main():
    root = tk.Tk()
    app = MazeSolverGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
