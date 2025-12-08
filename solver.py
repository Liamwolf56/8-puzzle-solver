import heapq
import copy

# The goal state for a standard 8-puzzle (0 represents the empty tile)
GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

class PuzzleState:
    def __init__(self, board, parent=None, move="Start"):
        self.board = board
        self.parent = parent
        self.move = move
        self.g = 0  # Cost from start to current
        self.h = 0  # Heuristic cost to goal
    
    @property
    def f(self):
        return self.g + self.h

    def __lt__(self, other):
        # Required for the Priority Queue to compare states based on f-score
        return self.f < other.f

    def get_blank_index(self):
        return self.board.index(0)

    def is_goal(self):
        return self.board == GOAL_STATE

    def __str__(self):
        # Visualizing the board
        s = self.board
        return f"\n{s[0]} {s[1]} {s[2]}\n{s[3]} {s[4]} {s[5]}\n{s[6]} {s[7]} {s[8]}\n"

def manhattan_distance(board):
    """
    Calculates the sum of the distances of the tiles from their goal positions.
    """
    distance = 0
    for i in range(9):
        tile = board[i]
        if tile == 0: continue # Don't calculate for the empty tile
        
        # Current (x, y)
        x_current, y_current = i % 3, i // 3
        
        # Goal (x, y) - Note: tile value '1' is at index 0, '2' at 1...
        goal_index = tile - 1 
        x_goal, y_goal = goal_index % 3, goal_index // 3
        
        distance += abs(x_current - x_goal) + abs(y_current - y_goal)
    return distance

def get_neighbors(state):
    neighbors = []
    blank_idx = state.get_blank_index()
    x, y = blank_idx % 3, blank_idx // 3
    
    # Possible moves: Up, Down, Left, Right
    moves = [('Up', -3), ('Down', 3), ('Left', -1), ('Right', 1)]
    
    for direction, shift in moves:
        # Check boundary conditions
        if direction == 'Left' and x == 0: continue
        if direction == 'Right' and x == 2: continue
        if direction == 'Up' and y == 0: continue
        if direction == 'Down' and y == 2: continue
        
        new_board = list(state.board)
        # Swap blank with target
        new_board[blank_idx], new_board[blank_idx + shift] = \
            new_board[blank_idx + shift], new_board[blank_idx]
            
        neighbors.append(PuzzleState(tuple(new_board), state, direction))
        
    return neighbors

def solve_puzzle(start_board):
    # Priority Queue: Stores tuples of (cost, state)
    open_list = []
    start_state = PuzzleState(start_board)
    start_state.h = manhattan_distance(start_board)
    
    heapq.heappush(open_list, start_state)
    
    # Visited set to store board configurations we've already seen
    visited = set()
    visited.add(start_board)
    
    nodes_explored = 0

    print("Searching for solution...")

    while open_list:
        current_state = heapq.heappop(open_list)
        nodes_explored += 1
        
        if current_state.is_goal():
            return reconstruct_path(current_state), nodes_explored
        
        for neighbor in get_neighbors(current_state):
            if neighbor.board in visited:
                continue
            
            neighbor.g = current_state.g + 1
            neighbor.h = manhattan_distance(neighbor.board)
            visited.add(neighbor.board)
            
            heapq.heappush(open_list, neighbor)
            
    return None, nodes_explored

def reconstruct_path(state):
    path = []
    while state:
        path.append(state)
        state = state.parent
    return path[::-1]

if __name__ == "__main__":
    # Example solvable board (0 is blank)
    # 1 2 3
    # 4 0 5
    # 7 8 6
    start_board = (1, 2, 3, 4, 0, 5, 7, 8, 6)
    
    print("Start State:")
    print(PuzzleState(start_board))
    
    solution, explored = solve_puzzle(start_board)
    
    if solution:
        print(f"Solution found in {len(solution)-1} moves!")
        print(f"Nodes explored: {explored}")
        print("-" * 20)
        for step in solution:
            print(f"Move: {step.move}")
            print(step)
    else:
        print("No solution found.")
