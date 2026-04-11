"""
Best First Search Algorithm
Uses Priority Queue with only heuristic h(n)
"""
import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def best_first(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), start))
    
    visited = set([start])
    parent = {start: None}
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            return reconstruct_path(parent, start, goal), list(visited)
        
        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            neighbor = (nx, ny)
            
            if (0 <= nx < rows and 0 <= ny < cols and 
                neighbor not in visited and grid[nx][ny] != 1):
                
                visited.add(neighbor)
                parent[neighbor] = current
                h_score = heuristic(neighbor, goal)
                heapq.heappush(open_set, (h_score, neighbor))
    
    return None, list(visited)

def reconstruct_path(parent, start, goal):
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent[current]
    return path[::-1]
