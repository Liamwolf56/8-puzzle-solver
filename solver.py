import heapq

# --- Configuration ---
# The goal state for a standard 8-puzzle (0 represents the empty tile)
GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# --- Puzzle State Class (Node) ---
class PuzzleState:
    """Represents a state in the puzzle search space."""
    def __init__(self, board, parent=None, move="Start"):
        self.board = board      # Immutable tuple representing the 3x3 grid
        self.parent = parent    # Parent state for path reconstruction
        self.move = move        # The move (Up, Down, Left, Right) that led here
        self.g = 0              # Cost from start to current state (number of moves)
        self.h = 0              # Heuristic cost to goal
    
    @property
    def f(self):
        """Total estimated cost: f(n) = g(n) + h(n)"""
        return self.g + self.h

    def __lt__(self, other):
        """Required for the Priority Queue to compare states based on f-score."""
        return self.f < other.f

    def get_blank_index(self):
        """Finds the index of the blank tile (0)."""
        return self.board.index(0)

    def is_goal(self):
        """Checks if the current state matches the GOAL_STATE."""
        return self.board == GOAL_STATE

    def __str__(self):
        """Visualizing the board in a 3x3 grid format."""
        s = self.board
        return f"\n{s[0]} {s[1]} {s[2]}\n{s[3]} {s[4]} {s[5]}\n{s[6]} {s[7]} {s[8]}\n"

# --- Heuristic and Utility Functions ---

def manhattan_distance(board):
    """
    Calculates the Manhattan Distance (sum of absolute differences of current and goal positions).
    This is the admissible heuristic h(n).
    """
    distance = 0
    for i in range(9):
        tile = board[i]
        if tile == 0: continue
        
        # Current (x, y) coordinates
        x_current, y_current = i % 3, i // 3
        
        # Goal index and (x, y) coordinates
        goal_index = tile - 1 # Tile '1' goes to index 0, '2' to 1, etc.
        x_goal, y_goal = goal_index % 3, goal_index // 3
        
        distance += abs(x_current - x_goal) + abs(y_current - y_goal)
    return distance

def get_neighbors(state):
    """Generates all possible next states (neighbors) by sliding the blank tile."""
    neighbors = []
    blank_idx = state.get_blank_index()
    x, y = blank_idx % 3, blank_idx // 3
    
    # Possible moves: (Direction, index_shift)
    moves = [('Up', -3), ('Down', 3), ('Left', -1), ('Right', 1)]
    
    for direction, shift in moves:
        # Check boundary conditions based on current x, y
        if direction == 'Left' and x == 0: continue
        if direction == 'Right' and x == 2: continue
        if direction == 'Up' and y == 0: continue
        if direction == 'Down' and y == 2: continue
        
        # Create the new board configuration
        new_board_list = list(state.board)
        target_idx = blank_idx + shift
        
        # Swap blank with target tile
        new_board_list[blank_idx], new_board_list[target_idx] = \
            new_board_list[target_idx], new_board_list[blank_idx]
            
        neighbors.append(PuzzleState(tuple(new_board_list), state, direction))
        
    return neighbors

# --- Solvability Check Feature ---

def get_inversions(board):
    """Calculates the number of inversions in the board (excluding 0)."""
    inversions = 0
    # Create a 1D list of tiles, excluding the blank (0)
    tiles = [i for i in board if i != 0]
    
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1
    return inversions

def is_solvable(board):
    """
    Checks if the 8-puzzle is solvable. 
    For odd-width puzzles (like 3x3), it's solvable iff the number of inversions is even.
    """
    return get_inversions(board) % 2 == 0

# --- A* Search Solver ---

def solve_puzzle(start_board):
    """
    Runs the A* search algorithm to find the shortest path to the goal state.
    """
    # 1. Solvability Check
    if not is_solvable(start_board):
        return "Unsolvable", 0 
        
    # 2. A* Initialization
    # Priority Queue: Stores PuzzleState objects, sorted by f-score
    open_list = []
    start_state = PuzzleState(start_board)
    start_state.h = manhattan_distance(start_board)
    
    heapq.heappush(open_list, start_state)
    
    # Visited set: Stores board configurations (tuples) we've already seen
    visited = {start_board}
    
    nodes_explored = 0

    print("Searching for solution...")

    # 3. A* Main Loop
    while open_list:
        current_state = heapq.heappop(open_list)
        nodes_explored += 1
        
        if current_state.is_goal():
            return reconstruct_path(current_state), nodes_explored
        
        for neighbor in get_neighbors(current_state):
            if neighbor.board in visited:
                continue
            
            # Update costs (g is +1 because each move has a cost of 1)
            neighbor.g = current_state.g + 1
            neighbor.h = manhattan_distance(neighbor.board)
            visited.add(neighbor.board)
            
            heapq.heappush(open_list, neighbor)
            
    return None, nodes_explored # Should not be reached for solvable puzzles

# --- Path Reconstruction ---

def reconstruct_path(state):
    """Traces back the parent pointers from the goal state to the start state."""
    path = []
    while state:
        path.append(state)
        state = state.parent
    return path[::-1] # Reverse the path to show Start -> Goal

# --- Execution ---

if __name__ == "__main__":
    # --- Solvable Example ---
    # The default example solved in 2 moves:
    # 1 2 3
    # 4 0 5
    # 7 8 6
    solvable_board = (1, 2, 3, 4, 0, 5, 7, 8, 6)
    
    # --- Unsolvable Example ---
    # Swapping 8 and 6 from the solvable example results in an odd inversion count
    unsolvable_board = (1, 2, 3, 4, 0, 5, 7, 6, 8) 
    
    # Choose which board to solve
    start_board = solvable_board 
    
    print("--- 8-Puzzle A* Solver ---")
    print("Start State:")
    print(PuzzleState(start_board))
    
    solution, explored = solve_puzzle(start_board)
    
    if solution == "Unsolvable":
        print("-" * 20)
        print("ALERT: This puzzle configuration is mathematically unsolvable (Odd number of inversions).")
    elif solution:
        print(f"Solution found in {len(solution)-1} moves!")
        print(f"Nodes explored: {explored}")
        print("-" * 20)
        
        # Print solution path
        for step in solution:
            print(f"Move: {step.move}")
            print(step)
    else:
        print("No solution found.")
