"""
Hill Climbing Algorithm
Greedy local search - always moves to best neighbor
"""

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def hill_climbing(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    current = start
    visited = [start]
    path = [start]
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while current != goal:
        neighbors = []
        
        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            
            if (0 <= nx < rows and 0 <= ny < cols and 
                grid[nx][ny] != 1 and (nx, ny) not in visited):
                h = heuristic((nx, ny), goal)
                neighbors.append((h, (nx, ny)))
        
        if not neighbors:
            return None, visited
        
        neighbors.sort()
        _, best_neighbor = neighbors[0]
        
        current = best_neighbor
        visited.append(current)
        path.append(current)
    
    return path, visited
