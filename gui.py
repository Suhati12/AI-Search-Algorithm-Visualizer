"""
GUI Interface - AI Search Algorithm Visualizer
Bright colorful theme, animated visualization, compare all, maze generator
"""
import tkinter as tk
from tkinter import messagebox
import time
from bfs import bfs
from dfs import dfs
from astar import astar
from best_first import best_first
from hill_climbing import hill_climbing


# ── Color Palette (Light & Vibrant) ─────────────────────────────────────────
BG         = "#f0f4ff"
PANEL_BG   = "#ffffff"
HEADER_BG  = "#4f46e5"
BTN_RUN    = "#22c55e"
BTN_CMP    = "#f97316"
BTN_CLR    = "#94a3b8"
TEXT_DARK  = "#1e293b"
TEXT_MID   = "#475569"
TEXT_LIGHT = "#ffffff"
BORDER     = "#e2e8f0"

CELL_COLORS = {
    0: "#f8fafc",   # empty  — near white
    1: "#334155",   # wall   — dark slate
    2: "#16a34a",   # start  — green
    3: "#dc2626",   # goal   — red
    4: "#bfdbfe",   # visited — light blue
    5: "#fde68a",   # path   — yellow
    6: "#67e8f9",   # frontier — cyan
}

ALGO_COLORS = {
    "BFS":           "#3b82f6",
    "DFS":           "#a855f7",
    "A*":            "#22c55e",
    "Best First":    "#f97316",
    "Hill Climbing": "#eab308",
}


class PathfindingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Search Algorithm Visualizer")
        self.root.configure(bg=BG)
        self.root.geometry("1300x820")
        self.root.resizable(True, True)

        self.rows = 25
        self.cols = 30
        self.cell_size = 22
        self.grid = [[0] * self.cols for _ in range(self.rows)]
        self.start = None
        self.goal  = None
        self.drawing_mode = "wall"
        self.animation_speed = 20
        self.animating = False
        self._anim_job = None
        self.history = {}

        self.setup_ui()

    # ── UI BUILD ─────────────────────────────────────────────────────────────

    def setup_ui(self):
        # Header bar
        header = tk.Frame(self.root, bg=HEADER_BG, pady=10)
        header.pack(fill=tk.X)
        tk.Label(header, text="🔍  AI Search Algorithm Visualizer",
                 font=("Segoe UI", 17, "bold"),
                 bg=HEADER_BG, fg=TEXT_LIGHT).pack(side=tk.LEFT, padx=20)
        tk.Label(header, text="Python  ·  Tkinter  ·  heapq  ·  time",
                 font=("Segoe UI", 9),
                 bg=HEADER_BG, fg="#c7d2fe").pack(side=tk.RIGHT, padx=20)

        # Body
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill=tk.BOTH, expand=True, padx=14, pady=10)

        self._build_left_panel(body)
        self._build_canvas_area(body)

    def _section(self, parent, title):
        tk.Label(parent, text=title,
                 font=("Segoe UI", 9, "bold"),
                 bg=PANEL_BG, fg=HEADER_BG).pack(anchor=tk.W, padx=12, pady=(12, 2))
        tk.Frame(parent, bg=HEADER_BG, height=2).pack(fill=tk.X, padx=12)

    def _build_left_panel(self, parent):
        lf = tk.Frame(parent, bg=PANEL_BG, width=245,
                      relief=tk.FLAT, bd=0,
                      highlightthickness=1, highlightbackground=BORDER)
        lf.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))
        lf.pack_propagate(False)

        # ── Drawing mode ──
        self._section(lf, "DRAWING MODE")
        self.mode_var = tk.StringVar(value="wall")
        modes = [("🟢  Set Start", "start"),
                 ("🔴  Set Goal",  "goal"),
                 ("⬛  Add Wall",  "wall"),
                 ("⬜  Erase",     "erase")]
        for txt, val in modes:
            tk.Radiobutton(lf, text=txt, variable=self.mode_var, value=val,
                           bg=PANEL_BG, fg=TEXT_DARK,
                           selectcolor="#e0e7ff",
                           activebackground=PANEL_BG,
                           font=("Segoe UI", 9),
                           command=lambda v=val: setattr(self, 'drawing_mode', v)
                           ).pack(anchor=tk.W, padx=16, pady=2)

        # ── Algorithm ──
        self._section(lf, "ALGORITHM")
        self.algorithm_var = tk.StringVar(value="BFS")
        algos = [("BFS",           "BFS"),
                 ("DFS",           "DFS"),
                 ("A* Search",     "A*"),
                 ("Best First",    "Best First"),
                 ("Hill Climbing", "Hill Climbing")]
        for txt, val in algos:
            color = ALGO_COLORS.get(val, TEXT_DARK)
            tk.Radiobutton(lf, text=txt, variable=self.algorithm_var, value=val,
                           bg=PANEL_BG, fg=color,
                           selectcolor="#e0e7ff",
                           activebackground=PANEL_BG,
                           font=("Segoe UI", 9, "bold"),
                           ).pack(anchor=tk.W, padx=16, pady=2)

        # ── Speed ──
        self._section(lf, "ANIMATION SPEED")
        sf = tk.Frame(lf, bg=PANEL_BG)
        sf.pack(fill=tk.X, padx=12, pady=4)
        tk.Label(sf, text="Fast", bg=PANEL_BG, fg=TEXT_MID,
                 font=("Segoe UI", 8)).pack(side=tk.LEFT)
        self.speed_var = tk.IntVar(value=20)
        tk.Scale(sf, from_=1, to=200, orient=tk.HORIZONTAL,
                 variable=self.speed_var, bg=PANEL_BG, fg=TEXT_DARK,
                 troughcolor="#e0e7ff", highlightthickness=0,
                 command=lambda v: setattr(self, 'animation_speed', int(v))
                 ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(sf, text="Slow", bg=PANEL_BG, fg=TEXT_MID,
                 font=("Segoe UI", 8)).pack(side=tk.LEFT)

        # ── Buttons ──
        self._section(lf, "ACTIONS")
        buttons = [
            ("▶  Run Algorithm",         self.run_algorithm,  BTN_RUN,  TEXT_LIGHT),
            ("⚡  Compare All",           self.compare_all,    BTN_CMP,  TEXT_LIGHT),
            ("🗑  Clear Path",            self.clear_path,     BTN_CLR,  TEXT_LIGHT),
            ("✖  Clear Grid",            self.clear_grid,     "#ef4444", TEXT_LIGHT),
        ]
        for txt, cmd, bg, fg in buttons:
            tk.Button(lf, text=txt, command=cmd,
                      bg=bg, fg=fg,
                      font=("Segoe UI", 9, "bold"),
                      relief=tk.FLAT, pady=6,
                      activebackground=HEADER_BG,
                      activeforeground=TEXT_LIGHT,
                      cursor="hand2"
                      ).pack(fill=tk.X, padx=12, pady=3)

        # ── Results ──
        self._section(lf, "RESULTS")
        self.result_text = tk.Text(lf, height=11,
                                   bg="#f1f5f9", fg=TEXT_DARK,
                                   font=("Courier New", 9),
                                   relief=tk.FLAT,
                                   insertbackground=TEXT_DARK)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=12, pady=(4, 12))

    def _build_canvas_area(self, parent):
        right = tk.Frame(parent, bg=BG)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Legend
        legend = tk.Frame(right, bg=BG)
        legend.pack(fill=tk.X, pady=(0, 6))
        items = [("Start",    CELL_COLORS[2]),
                 ("Goal",     CELL_COLORS[3]),
                 ("Wall",     CELL_COLORS[1]),
                 ("Visited",  CELL_COLORS[4]),
                 ("Path",     CELL_COLORS[5]),
                 ("Frontier", CELL_COLORS[6])]
        for label, color in items:
            f = tk.Frame(legend, bg=BG)
            f.pack(side=tk.LEFT, padx=8)
            tk.Frame(f, bg=color, width=16, height=16,
                     highlightthickness=1,
                     highlightbackground=BORDER).pack(side=tk.LEFT)
            tk.Label(f, text=f" {label}", bg=BG, fg=TEXT_DARK,
                     font=("Segoe UI", 9)).pack(side=tk.LEFT)

        # Canvas
        cw = self.cols * self.cell_size
        ch = self.rows * self.cell_size
        self.canvas = tk.Canvas(right, width=cw, height=ch,
                                bg=CELL_COLORS[0],
                                highlightthickness=2,
                                highlightbackground=HEADER_BG)
        self.canvas.pack()
        self.canvas.bind("<Button-1>",  self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)

        # Status bar
        self.status_var = tk.StringVar(value="Ready — set Start, Goal, draw walls, then Run.")
        tk.Label(right, textvariable=self.status_var,
                 bg=BG, fg=TEXT_MID,
                 font=("Segoe UI", 9)).pack(anchor=tk.W, pady=4)

        self.draw_grid()

    # ── GRID DRAWING ─────────────────────────────────────────────────────────

    def draw_grid(self):
        self.canvas.delete("all")
        cs = self.cell_size
        for i in range(self.rows):
            for j in range(self.cols):
                x1, y1 = j * cs, i * cs
                color = CELL_COLORS[self.grid[i][j]]
                self.canvas.create_rectangle(x1, y1, x1+cs, y1+cs,
                                             fill=color, outline="#e2e8f0", width=1)
        if self.start:
            r, c = self.start
            cx, cy = c*cs + cs//2, r*cs + cs//2
            self.canvas.create_text(cx, cy, text="S",
                                    fill="white", font=("Segoe UI", 8, "bold"))
        if self.goal:
            r, c = self.goal
            cx, cy = c*cs + cs//2, r*cs + cs//2
            self.canvas.create_text(cx, cy, text="G",
                                    fill="white", font=("Segoe UI", 8, "bold"))

    def _draw_cell(self, row, col, state):
        cs = self.cell_size
        x1, y1 = col*cs, row*cs
        self.canvas.create_rectangle(x1, y1, x1+cs, y1+cs,
                                     fill=CELL_COLORS[state],
                                     outline="#e2e8f0", width=1)

    # ── MOUSE ────────────────────────────────────────────────────────────────

    def on_click(self, event): self.handle_cell(event)
    def on_drag(self,  event): self.handle_cell(event)

    def handle_cell(self, event):
        if self.animating:
            return
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return

        mode = self.mode_var.get()
        self.drawing_mode = mode

        if mode == "start":
            if self.start:
                self.grid[self.start[0]][self.start[1]] = 0
            self.start = (row, col)
            self.grid[row][col] = 2
        elif mode == "goal":
            if self.goal:
                self.grid[self.goal[0]][self.goal[1]] = 0
            self.goal = (row, col)
            self.grid[row][col] = 3
        elif mode == "wall":
            if (row, col) not in (self.start, self.goal):
                self.grid[row][col] = 1
        elif mode == "erase":
            if (row, col) == self.start:  self.start = None
            elif (row, col) == self.goal: self.goal  = None
            self.grid[row][col] = 0

        self.draw_grid()

    # ── CLEAR ────────────────────────────────────────────────────────────────

    def clear_path(self):
        self._stop_animation()
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] in (4, 5, 6):
                    self.grid[i][j] = 0
        self.draw_grid()

    def clear_grid(self):
        self._stop_animation()
        self.grid  = [[0]*self.cols for _ in range(self.rows)]
        self.start = None
        self.goal  = None
        self.history = {}
        self.draw_grid()
        self.result_text.delete(1.0, tk.END)
        self.status_var.set("Grid cleared.")

    # ── ANIMATION ────────────────────────────────────────────────────────────

    def _stop_animation(self):
        if self._anim_job:
            self.root.after_cancel(self._anim_job)
            self._anim_job = None
        self.animating = False

    def _animate(self, visited_seq, path, algo, elapsed, nodes_total):
        self.animating = True
        idx = [0]

        def step():
            if idx[0] < len(visited_seq):
                node = visited_seq[idx[0]]
                if self.grid[node[0]][node[1]] not in (2, 3):
                    self.grid[node[0]][node[1]] = 6
                    self._draw_cell(node[0], node[1], 6)
                idx[0] += 1
                self._anim_job = self.root.after(self.animation_speed, step)
            else:
                if path:
                    for node in path:
                        if self.grid[node[0]][node[1]] not in (2, 3):
                            self.grid[node[0]][node[1]] = 5
                            self._draw_cell(node[0], node[1], 5)
                self.draw_grid()
                self.animating = False
                self._show_result(algo, nodes_total, elapsed,
                                  len(path) if path else None)

        step()

    # ── RUN ALGORITHM ────────────────────────────────────────────────────────

    def run_algorithm(self):
        if not self.start or not self.goal:
            messagebox.showwarning("Missing", "Please set Start and Goal first!")
            return
        self.clear_path()
        algo = self.algorithm_var.get()
        self.status_var.set(f"Running {algo}…")
        self.root.update()

        path, visited, elapsed = self._execute(algo)
        self._animate(visited, path, algo, elapsed, len(visited))

    def _execute(self, algo):
        t0 = time.perf_counter()
        if   algo == "BFS":           path, visited = bfs(self.grid, self.start, self.goal)
        elif algo == "DFS":           path, visited = dfs(self.grid, self.start, self.goal)
        elif algo == "A*":            path, visited = astar(self.grid, self.start, self.goal)
        elif algo == "Best First":    path, visited = best_first(self.grid, self.start, self.goal)
        elif algo == "Hill Climbing": path, visited = hill_climbing(self.grid, self.start, self.goal)
        else:                         path, visited = [], []
        elapsed = (time.perf_counter() - t0) * 1000
        return path or [], visited or [], elapsed

    def _show_result(self, algo, nodes, elapsed, path_len):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"{'─'*30}\n")
        self.result_text.insert(tk.END, f" Algorithm  : {algo}\n")
        self.result_text.insert(tk.END, f" Nodes      : {nodes}\n")
        self.result_text.insert(tk.END, f" Time       : {elapsed:.3f} ms\n")
        self.result_text.insert(tk.END, f" Path Len   : {path_len if path_len else 'No path'}\n")
        self.result_text.insert(tk.END, f"{'─'*30}\n")
        self.status_var.set(
            f"{algo} — {nodes} nodes visited, {elapsed:.2f} ms, "
            f"path = {path_len if path_len else 'not found'}")

    # ── COMPARE ALL ──────────────────────────────────────────────────────────

    def compare_all(self):
        if not self.start or not self.goal:
            messagebox.showwarning("Missing", "Please set Start and Goal first!")
            return
        self._stop_animation()
        self.clear_path()

        algos   = ["BFS", "DFS", "A*", "Best First", "Hill Climbing"]
        results = {}

        for algo in algos:
            path, visited, elapsed = self._execute(algo)
            results[algo] = {
                "nodes": len(visited),
                "time":  elapsed,
                "path":  len(path) if path else None,
            }

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"{'─'*36}\n")
        self.result_text.insert(tk.END,
            f" {'Algorithm':<14} {'Nodes':>6} {'ms':>8} {'Path':>6}\n")
        self.result_text.insert(tk.END, f"{'─'*36}\n")

        valid = {a: d for a, d in results.items() if d["path"]}
        best  = min(valid, key=lambda a: valid[a]["path"]) if valid else None

        for algo, d in results.items():
            star = " ★" if algo == best else ""
            pl   = str(d["path"]) if d["path"] else "None"
            self.result_text.insert(tk.END,
                f" {algo:<14} {d['nodes']:>6} {d['time']:>7.2f} {pl:>6}{star}\n")

        self.result_text.insert(tk.END, f"{'─'*36}\n")
        if best:
            self.result_text.insert(tk.END, f" ★ Best path: {best}\n")

        if best:
            path, visited, elapsed = self._execute(best)
            self._animate(visited, path, best,
                          results[best]["time"], results[best]["nodes"])
        self.status_var.set(f"Comparison done. Best path algorithm: {best}")


