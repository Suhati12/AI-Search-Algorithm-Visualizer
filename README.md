# AI Search Algorithm Visualizer

A Python GUI application that visualizes and compares various AI search algorithms for pathfinding in a maze.

# Features

- Interactive grid/maze creation (20x20)
- Multiple search algorithms:
  - Breadth First Search (BFS)
  - Depth First Search (DFS)
  - A* Search
  - Best First Search
  - Hill Climbing
- Real-time visualization of algorithm execution
- Performance comparison (nodes visited, time, path length)
- Tic-Tac-Toe game with Minimax and Alpha-Beta Pruning

# Installation

```bash
# No external dependencies required - uses Python standard library
python main.py
```

# Usage

1. Set start point (green) by selecting "Set Start" and clicking on grid
2. Set goal point (red) by selecting "Set Goal" and clicking on grid
3. Add walls (black) by selecting "Add Wall" and drawing on grid
4. Select an algorithm from the dropdown
5. Click "Run Algorithm" to visualize
6. View results: nodes visited, time taken, path length

# Data Structures Used

| Algorithm | Data Structure |
|-----------|---------------|
| BFS | Queue (deque) |
| DFS | Stack (list) |
| A* | Priority Queue (heapq) |
| Best First | Priority Queue (heapq) |
| Hill Climbing | Greedy selection |
| Minimax | Game tree |
| Alpha-Beta | Tree with pruning |

# Color Legend

- Green: Start point
- Red: Goal point
- Black: Walls/obstacles
- Light Blue: Visited nodes
- Yellow: Final path
- White: Empty cells

# Project Structure

```
AI_Search_Project/
├── main.py              # Entry point
├── gui.py               # GUI interface
├── bfs.py               # BFS implementation
├── dfs.py               # DFS implementation
├── astar.py             # A* implementation
├── best_first.py        # Best First implementation
├── hill_climbing.py     # Hill Climbing implementation
├── minimax.py           # Minimax & Alpha-Beta for Tic-Tac-Toe
└── README.md            # Documentation
```

## Algorithms Explained

## BFS (Breadth First Search)
- Uses Queue (FIFO)
- Explores level by level
- Guarantees shortest path
- Complete and optimal

## DFS (Depth First Search)
- Uses Stack (LIFO)
- Explores depth first
- May not find shortest path
- Memory efficient

## A* Search
- Uses Priority Queue with f(n) = g(n) + h(n)
- g(n): cost from start
- h(n): heuristic (Manhattan distance)
- Optimal and efficient

## Best First Search
- Uses Priority Queue with only h(n)
- Greedy approach
- Not guaranteed optimal
- Fast but may miss better paths

## Hill Climbing
- Local search algorithm
- Always moves to best neighbor
- Can get stuck in local optima
- Simple and fast

## Minimax
- Game tree algorithm
- Assumes optimal opponent play
- Used in Tic-Tac-Toe AI

## Alpha-Beta Pruning
- Optimization of Minimax
- Prunes unnecessary branches
- Same result, faster execution

# Technologies Used

- **Language**: Python 3
- **GUI**: Tkinter
- **Libraries**: heapq, time, collections
- **Data Structures**: Graph, Queue, Stack, Priority Queue, Tree
