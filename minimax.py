"""
Minimax and Alpha-Beta Pruning — Tic-Tac-Toe
Bright colorful theme
"""
import tkinter as tk
from tkinter import messagebox
import math

BG      = "#f0f4ff"
PANEL   = "#ffffff"
HEADER  = "#4f46e5"
BTN     = "#e0e7ff"
TEXT    = "#1e293b"
SUBTEXT = "#64748b"
X_COLOR = "#3b82f6"
O_COLOR = "#ef4444"
GREEN   = "#22c55e"
BORDER  = "#e2e8f0"


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe — Minimax AI")
        self.root.geometry("460x600")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.board  = [' '] * 9
        self.human  = 'X'
        self.ai     = 'O'
        self.use_ab = tk.BooleanVar(value=True)
        self.scores = {"You": 0, "AI": 0, "Draw": 0}

        self._build_ui()

    def _build_ui(self):
        # Header
        hdr = tk.Frame(self.root, bg=HEADER, pady=12)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text="🎮  Tic-Tac-Toe AI",
                 font=("Segoe UI", 16, "bold"),
                 bg=HEADER, fg="white").pack()
        tk.Label(hdr, text="Minimax  ·  Alpha-Beta Pruning",
                 font=("Segoe UI", 9), bg=HEADER, fg="#c7d2fe").pack()

        # Toggle
        tf = tk.Frame(self.root, bg=BG)
        tf.pack(pady=10)
        tk.Checkbutton(tf, text="Use Alpha-Beta Pruning",
                       variable=self.use_ab,
                       bg=BG, fg=TEXT,
                       selectcolor=BTN,
                       activebackground=BG,
                       font=("Segoe UI", 10)).pack()

        # Score
        self.score_var = tk.StringVar()
        self._update_score()
        tk.Label(self.root, textvariable=self.score_var,
                 font=("Segoe UI", 11, "bold"),
                 bg=BG, fg=HEADER).pack(pady=4)

        # Board
        board_outer = tk.Frame(self.root, bg=HEADER, padx=3, pady=3)
        board_outer.pack(pady=6)
        board_inner = tk.Frame(board_outer, bg=BORDER)
        board_inner.pack()

        self.buttons = []
        for i in range(9):
            btn = tk.Button(board_inner, text=' ',
                            font=("Segoe UI", 28, "bold"),
                            width=4, height=2,
                            bg=PANEL, fg=TEXT,
                            relief=tk.FLAT,
                            activebackground="#e0e7ff",
                            cursor="hand2",
                            command=lambda idx=i: self.human_move(idx))
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)
            self.buttons.append(btn)

        # Status
        self.status_var = tk.StringVar(value="Your turn! Click a cell.")
        tk.Label(self.root, textvariable=self.status_var,
                 font=("Segoe UI", 11), bg=BG, fg=TEXT).pack(pady=8)

        # Reset
        tk.Button(self.root, text="New Game",
                  command=self.reset_game,
                  bg=HEADER, fg="white",
                  font=("Segoe UI", 11, "bold"),
                  relief=tk.FLAT, padx=24, pady=8,
                  cursor="hand2",
                  activebackground="#4338ca",
                  activeforeground="white"
                  ).pack(pady=4)

    def _update_score(self):
        s = self.scores
        self.score_var.set(f"You: {s['You']}   AI: {s['AI']}   Draw: {s['Draw']}")

    def human_move(self, idx):
        if self.board[idx] != ' ':
            return
        self.board[idx] = self.human
        self.buttons[idx].config(text=self.human, fg=X_COLOR, state='disabled')

        if self.check_winner(self.board, self.human):
            self._end_game("You win! 🎉", "You")
            return
        if ' ' not in self.board:
            self._end_game("It's a draw!", "Draw")
            return

        self.status_var.set("AI is thinking…")
        self.root.update()
        self.root.after(250, self.ai_move)

    def ai_move(self):
        if self.use_ab.get():
            _, move = self.alpha_beta(self.board, 0, True, -math.inf, math.inf)
        else:
            _, move = self.minimax(self.board, 0, True)

        if move is not None:
            self.board[move] = self.ai
            self.buttons[move].config(text=self.ai, fg=O_COLOR, state='disabled')

            if self.check_winner(self.board, self.ai):
                self._end_game("AI wins! 🤖", "AI")
                return
            if ' ' not in self.board:
                self._end_game("It's a draw!", "Draw")
                return

        self.status_var.set("Your turn!")

    def _end_game(self, msg, winner):
        self.scores[winner] += 1
        self._update_score()
        self.status_var.set(msg)
        for btn in self.buttons:
            btn.config(state='disabled')
        self.root.after(1200, lambda: messagebox.showinfo("Game Over", msg, parent=self.root))

    def minimax(self, board, depth, is_max):
        if self.check_winner(board, self.ai):    return 10 - depth, None
        if self.check_winner(board, self.human): return depth - 10, None
        if ' ' not in board:                     return 0, None

        best = -math.inf if is_max else math.inf
        best_move = None
        player = self.ai if is_max else self.human

        for i in range(9):
            if board[i] == ' ':
                board[i] = player
                score, _ = self.minimax(board, depth+1, not is_max)
                board[i] = ' '
                if (is_max and score > best) or (not is_max and score < best):
                    best, best_move = score, i
        return best, best_move

    def alpha_beta(self, board, depth, is_max, alpha, beta):
        if self.check_winner(board, self.ai):    return 10 - depth, None
        if self.check_winner(board, self.human): return depth - 10, None
        if ' ' not in board:                     return 0, None

        best = -math.inf if is_max else math.inf
        best_move = None
        player = self.ai if is_max else self.human

        for i in range(9):
            if board[i] == ' ':
                board[i] = player
                score, _ = self.alpha_beta(board, depth+1, not is_max, alpha, beta)
                board[i] = ' '
                if is_max:
                    if score > best: best, best_move = score, i
                    alpha = max(alpha, score)
                else:
                    if score < best: best, best_move = score, i
                    beta = min(beta, score)
                if beta <= alpha:
                    break
        return best, best_move

    def check_winner(self, board, player):
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        return any(board[a]==board[b]==board[c]==player for a,b,c in wins)

    def reset_game(self):
        self.board = [' '] * 9
        for btn in self.buttons:
            btn.config(text=' ', state='normal', fg=TEXT)
        self.status_var.set("Your turn! Click a cell.")
