"""
Breadth First Search (BFS) Algorithm
Uses Queue data structure
"""
from collections import deque

def bfs(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    queue = deque([start])
    visited = set([start])
    parent = {start: None}
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while queue:
        current = queue.popleft()
        
        if current == goal:
            return reconstruct_path(parent, start, goal), list(visited)
        
        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            
            if (0 <= nx < rows and 0 <= ny < cols and 
                (nx, ny) not in visited and grid[nx][ny] != 1):
                queue.append((nx, ny))
                visited.add((nx, ny))
                parent[(nx, ny)] = current
    
    return None, list(visited)

def reconstruct_path(parent, start, goal):
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent[current]
    return path[::-1]
