# puzzle_gui.py (UPDATED for PDB)

import pygame
import sys
import random
# Import core logic and the PDB loading function
try:
    from solver import PuzzleState, solve_puzzle, is_solvable, GOAL_STATE, load_pdb
except ImportError:
    print("FATAL: Cannot import solver logic. Ensure 'solver.py' is in the same directory.")
    sys.exit()

# --- Pygame Setup ---
pygame.init()
WIDTH, HEIGHT = 600, 780  
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-Puzzle Solver Interactive (PDB)")

# --- Colors and Fonts ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
GREEN = (50, 200, 50)
RED = (200, 50, 50)
FONT_SIZE = 40
FONT = pygame.font.Font(None, FONT_SIZE)
SMALL_FONT = pygame.font.Font(None, 24)

# --- Board Dimensions ---
GRID_SIZE = 3
TILE_SIZE = WIDTH // GRID_SIZE
BOARD_RECT = pygame.Rect(0, 0, WIDTH, WIDTH)

# --- Global State ---
current_board_tuple = GOAL_STATE
solving_path = None
path_index = 0
solving = False
solving_results = None 
current_heuristic = "Manhattan Distance" # Legacy variable, now hardcoded to PDB/Manhattan

# --- Button Configuration (Fixed Positions) ---
BUTTON_Y = 610
BUTTON_H = 50
BUTTON_W = 160

SHUFFLE_RECT = pygame.Rect(40, BUTTON_Y, BUTTON_W, BUTTON_H) 
ACTION_RECT = pygame.Rect(220, BUTTON_Y, BUTTON_W, BUTTON_H)
RESET_RECT = pygame.Rect(400, BUTTON_Y, BUTTON_W, BUTTON_H)

# Info Label Position
INFO_LABEL_RECT = pygame.Rect(10, HEIGHT - 70, WIDTH - 20, 30)

# --- Drawing Functions ---

def draw_board(screen, board):
    """Draws the 3x3 grid and tiles."""
    screen.fill(LIGHT_GRAY, BOARD_RECT)
    
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            index = i * GRID_SIZE + j
            tile_value = board[index]
            
            x = j * TILE_SIZE
            y = i * TILE_SIZE
            
            tile_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, DARK_GRAY, tile_rect, 0)
            pygame.draw.rect(screen, BLACK, tile_rect, 3) 
            
            if tile_value != 0:
                text_surface = FONT.render(str(tile_value), True, WHITE)
                text_rect = text_surface.get_rect(center=tile_rect.center)
                screen.blit(text_surface, text_rect)

def draw_button(screen, rect, text, color):
    """Draws a clickable button."""
    pygame.draw.rect(screen, color, rect, 0, 10)
    text_surface = FONT.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def draw_info_label(screen):
    """Draws a single label showing the active heuristic mode (PDB)."""
    
    mode_text = SMALL_FONT.render("Mode: Puzzle Solver (H: Pattern Database)", True, BLACK)
    
    mode_rect = mode_text.get_rect(center=INFO_LABEL_RECT.center)
    screen.blit(mode_text, mode_rect)

def draw_scoreboard(screen):
    """Draws the performance results after a solve is complete."""
    global solving_results
    if not solving_results:
        return

    box_rect = pygame.Rect(50, HEIGHT - 110, WIDTH - 100, 70)
    pygame.draw.rect(screen, DARK_GRAY, box_rect, 0, 10)
    
    # Display PDB as the heuristic
    heuristic_text = SMALL_FONT.render(f"H: Pattern Database", True, WHITE)
    moves_text = SMALL_FONT.render(f"Moves: {solving_results['moves']}", True, WHITE)
    explored_text = SMALL_FONT.render(f"Nodes Explored: {solving_results['explored']}", True, WHITE)

    screen.blit(heuristic_text, (box_rect.left + 10, box_rect.top + 5))
    screen.blit(moves_text, (box_rect.left + 10, box_rect.top + 35))
    screen.blit(explored_text, (box_rect.right - explored_text.get_width() - 10, box_rect.top + 35))

# --- Game Logic Functions ---

def get_clicked_tile(pos):
    """Converts mouse position to grid index (row, col)."""
    if BOARD_RECT.collidepoint(pos):
        col = pos[0] // TILE_SIZE
        row = pos[1] // TILE_SIZE
        return row, col
    return None

def slide_tile(board, r1, c1):
    """Handles the sliding logic when a tile is clicked."""
    board_list = list(board)
    current_index = r1 * GRID_SIZE + c1
    blank_index = board_list.index(0)
    
    r_blank, c_blank = blank_index // GRID_SIZE, blank_index % GRID_SIZE
    
    dr = abs(r1 - r_blank)
    dc = abs(c1 - c_blank)
    
    if (dr == 1 and dc == 0) or (dr == 0 and dc == 1):
        board_list[current_index], board_list[blank_index] = \
            board_list[blank_index], board_list[current_index]
        return tuple(board_list)
        
    return board

def shuffle_board():
    """Generates a random, guaranteed solvable board."""
    while True:
        temp_list = [i for i in range(9)]
        random.shuffle(temp_list)
        temp_board = tuple(temp_list)
        if is_solvable(temp_board):
            return temp_board

def solve_and_prepare_path(board):
    """Triggers the A* solver using the PDB heuristic."""
    
    print("Solver initiated (Mode: PDB Solver)...")
    
    # Call the solver without the heuristic argument (it's hardcoded to PDB)
    solution_states, explored = solve_puzzle(board) 
    
    if solution_states == "Unsolvable":
        return None, None
    elif solution_states:
        moves = len(solution_states) - 1
        print(f"Solution found in {moves} moves. Nodes Explored: {explored}")
        
        # Report Pattern Database as the heuristic used
        results = {"moves": moves, "explored": explored, "heuristic": "Pattern Database"}
        return solution_states, results
    return None, None

# --- Main Game Loop ---
def main():
    global current_board_tuple, solving, solving_path, path_index, solving_results
    clock = pygame.time.Clock()
    
    current_board_tuple = shuffle_board()
    solving = False

    while True:
        SCREEN.fill(WHITE)
        
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                
                # Tile Click (Only if not solving)
                if not solving and BOARD_RECT.collidepoint(pos):
                    solving_results = None 
                    r, c = get_clicked_tile(pos)
                    if r is not None:
                        current_board_tuple = slide_tile(current_board_tuple, r, c)
                        if current_board_tuple == GOAL_STATE:
                            print("Puzzle Solved Manually!")

                # SHUFFLE
                if SHUFFLE_RECT.collidepoint(pos):
                    solving = False
                    solving_results = None
                    solving_path = None
                    path_index = 0
                    current_board_tuple = shuffle_board()
                
                # ACTION (SOLVE / NEXT STEP)
                elif ACTION_RECT.collidepoint(pos):
                    if not solving:
                        solving_path, results = solve_and_prepare_path(current_board_tuple)
                        if solving_path:
                            solving = True
                            solving_results = results
                            path_index = 0
                    else:
                        # NEXT STEP
                        if path_index < len(solving_path):
                            current_board_tuple = solving_path[path_index].board
                            path_index += 1
                            if path_index == len(solving_path):
                                 solving = False
                                 print("Solution Animation Complete (Stepped through)!")
                        
                # RESET
                elif solving and RESET_RECT.collidepoint(pos):
                    solving = False
                    if solving_path:
                        current_board_tuple = solving_path[0].board
                        solving_path = None
                        path_index = 0
                        print("Solving visualization reset.")
        
        # --- Drawing ---
        draw_board(SCREEN, current_board_tuple)
        
        draw_info_label(SCREEN) 
        draw_scoreboard(SCREEN)
        
        # Buttons
        draw_button(SCREEN, SHUFFLE_RECT, "SHUFFLE", DARK_GRAY)

        if not solving:
            draw_button(SCREEN, ACTION_RECT, "SOLVE (A*)", GREEN)
        else:
            if path_index < len(solving_path):
                 draw_button(SCREEN, ACTION_RECT, "NEXT STEP", GREEN)
            else:
                 draw_button(SCREEN, ACTION_RECT, "FINISHED", DARK_GRAY)

        if solving:
            draw_button(SCREEN, RESET_RECT, "STOP/RESET", RED)

        # Status Message 
        if current_board_tuple == GOAL_STATE:
            status_text = FONT.render("SOLVED!", True, GREEN)
        elif not solving and solving_results:
             status_text = FONT.render("PDB Metrics Above", True, BLACK)
        else:
            status_text = FONT.render("Ready to Play or Solve", True, BLACK)

        status_rect = status_text.get_rect(center=(WIDTH // 2, 685))
        SCREEN.blit(status_text, status_rect)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    # Load the PDB file before starting the main loop!
    try:
        load_pdb()
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Ensure 'pdb_generator.py' was run and 'pdb_6.dat' exists.")
        pygame.quit()
        sys.exit()
