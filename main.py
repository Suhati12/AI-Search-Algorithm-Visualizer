"""
AI Search Algorithm Visualizer — Entry Point
"""
import tkinter as tk
from gui import PathfindingGUI

def main():
    root = tk.Tk()
    root.resizable(True, True)
    app = PathfindingGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
