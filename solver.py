# solver.py (UPDATED for PDB)

import heapq
import collections
import pickle
import sys

# --- Constants ---
GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
PATTERN_TILES = {1, 2, 3, 4, 5, 6}

# --- PDB Global Data ---
PDB_6_DATA = {}

# --- Utility Class ---
class PuzzleState:
    """Represents a state of the 8-puzzle."""
    def __init__(self, board, parent=None, action=None, cost=0, heuristic_cost=0):
        self.board = board       # Tuple representing the board (e.g., (1, 2, 3, 4, 5, 6, 7, 8, 0))
        self.parent = parent     # Previous state in the path
        self.action = action     # Action taken to reach this state
        self.cost = cost         # g(n): moves from start to current state
        self.heuristic_cost = heuristic_cost # h(n): heuristic estimate
        self.f_cost = cost + heuristic_cost # f(n) = g(n) + h(n)

    def __lt__(self, other):
        """Used for priority queue comparison (f_cost)."""
        return self.f_cost < other.f_cost

    def __hash__(self):
        """Allows state to be used as a dictionary key."""
        return hash(self.board)

    def __eq__(self, other):
        """Allows comparison of states."""
        return self.board == other.board

# --- Heuristic and Utility Functions ---

def is_solvable(board):
    """Determines if the given board is solvable using inversion counting."""
    inversions = 0
    board_list = [i for i in board if i != 0]
    
    for i in range(len(board_list)):
        for j in range(i + 1, len(board_list)):
            if board_list[i] > board_list[j]:
                inversions += 1
                
    # 8-puzzle (3x3 grid) is solvable if the number of inversions is even.
    return inversions % 2 == 0

def get_neighbors(board):
    """Generates all valid neighbor board states."""
    board_list = list(board)
    zero_index = board_list.index(0)
    r, c = zero_index // 3, zero_index % 3
    
    neighbors = []
    moves = [('Up', -1, 0), ('Down', 1, 0), ('Left', 0, -1), ('Right', 0, 1)]
    
    for action, dr, dc in moves:
        new_r, new_c = r + dr, c + dc
        
        if 0 <= new_r < 3 and 0 <= new_c < 3:
            swap_index = new_r * 3 + new_c
            
            new_board_list = board_list[:]
            new_board_list[zero_index], new_board_list[swap_index] = \
                new_board_list[swap_index], new_board_list[zero_index]
            
            neighbors.append((tuple(new_board_list), action))
            
    return neighbors

def load_pdb():
    """Loads the pre-calculated PDB data from the file."""
    global PDB_6_DATA
    try:
        with open('pdb_6.dat', 'rb') as f:
            PDB_6_DATA = pickle.load(f)
        print("PDB (6-tile) loaded successfully for A* search.")
    except FileNotFoundError:
        print("PDB file 'pdb_6.dat' not found. Please run pdb_generator.py first.")
        sys.exit(1)

def pdb_heuristic(board):
    """
    PDB Heuristic: Looks up the exact minimum cost for the 6-tile pattern.
    """
    
    # 1. Create the unique key from the current board state
    # Key format: (pos_of_1, pos_of_2, ..., pos_of_6, pos_of_0)
    key_list = [0] * (len(PATTERN_TILES) + 1)
    
    for i, tile in enumerate(board):
        if tile in PATTERN_TILES:
            key_list[tile - 1] = i
        elif tile == 0:
            key_list[-1] = i
            
    key = tuple(key_list)
    
    # 2. Lookup the cost in the loaded global PDB data
    return PDB_6_DATA.get(key, 0) # Fallback to 0 if key error occurs

# --- A* Solver ---

def solve_puzzle(start_board): # NOTE: Heuristic argument is removed, PDB is hardcoded
    """A* search algorithm to find the shortest path to the goal."""
    if not is_solvable(start_board):
        return "Unsolvable", 0

    start_state = PuzzleState(start_board)
    
    # Initial cost calculation using the powerful PDB heuristic
    start_state.heuristic_cost = pdb_heuristic(start_state.board) 
    start_state.f_cost = start_state.cost + start_state.heuristic_cost
    
    # Priority Queue: stores states to be explored (f_cost is the priority)
    open_set = [start_state]
    # Dictionary for O(1) lookup of minimum cost found so far to reach a board state
    closed_set = {start_board: start_state.cost}
    
    explored_nodes = 0

    while open_set:
        current_state = heapq.heappop(open_set)
        explored_nodes += 1
        
        if current_state.board == GOAL_STATE:
            # Reconstruct path and return
            path = []
            while current_state:
                path.append(current_state)
                current_state = current_state.parent
            return path[::-1], explored_nodes # Return path from start to goal

        for neighbor_board, action in get_neighbors(current_state.board):
            new_cost = current_state.cost + 1
            
            # Check if this neighbor has already been reached with an equal or lower cost
            if neighbor_board in closed_set and new_cost >= closed_set[neighbor_board]:
                continue

            # This path is better, or the state is new
            closed_set[neighbor_board] = new_cost
            
            neighbor_state = PuzzleState(
                board=neighbor_board,
                parent=current_state,
                action=action,
                cost=new_cost,
            )
            
            # Calculate PDB heuristic cost for the neighbor
            neighbor_state.heuristic_cost = pdb_heuristic(neighbor_state.board)
            neighbor_state.f_cost = neighbor_state.cost + neighbor_state.heuristic_cost
            
            # Add to the open set
            heapq.heappush(open_set, neighbor_state)

    return None, explored_nodes
