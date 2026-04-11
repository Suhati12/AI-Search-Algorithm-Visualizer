"""
Depth First Search (DFS) Algorithm
Uses Stack data structure
"""

def dfs(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    stack = [start]
    visited = set([start])
    parent = {start: None}
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while stack:
        current = stack.pop()
        
        if current == goal:
            return reconstruct_path(parent, start, goal), list(visited)
        
        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            
            if (0 <= nx < rows and 0 <= ny < cols and 
                (nx, ny) not in visited and grid[nx][ny] != 1):
                stack.append((nx, ny))
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
