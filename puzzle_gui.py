# puzzle_gui.py

import pygame
import sys
import random
from solver import PuzzleState, manhattan_distance, solve_puzzle, is_solvable, GOAL_STATE

# --- Pygame Setup ---
pygame.init()
WIDTH, HEIGHT = 600, 680  # 600x600 for board, extra 80px for button
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-Puzzle Solver Interactive")

# --- Colors and Fonts ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
GREEN = (50, 200, 50)
FONT_SIZE = 40
FONT = pygame.font.Font(None, FONT_SIZE)

# --- Board Dimensions ---
GRID_SIZE = 3
TILE_SIZE = WIDTH // GRID_SIZE
BOARD_RECT = pygame.Rect(0, 0, WIDTH, WIDTH)

# --- Global State ---
current_board_tuple = GOAL_STATE
solving_path = None
path_index = 0
solving = False

# --- Button Configuration ---
SOLVE_BUTTON_RECT = pygame.Rect(50, 610, 200, 50)
SHUFFLE_BUTTON_RECT = pygame.Rect(350, 610, 200, 50)

# --- Functions ---

def draw_board(screen, board):
    """Draws the 3x3 grid and tiles."""
    screen.fill(LIGHT_GRAY, BOARD_RECT)
    
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            index = i * GRID_SIZE + j
            tile_value = board[index]
            
            x = j * TILE_SIZE
            y = i * TILE_SIZE
            
            # Draw the tile rectangle
            tile_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, DARK_GRAY, tile_rect, 0)
            pygame.draw.rect(screen, BLACK, tile_rect, 3) # Border
            
            if tile_value != 0:
                # Draw the number
                text_surface = FONT.render(str(tile_value), True, WHITE)
                text_rect = text_surface.get_rect(center=tile_rect.center)
                screen.blit(text_surface, text_rect)

def draw_button(screen, rect, text, color):
    """Draws a clickable button."""
    pygame.draw.rect(screen, color, rect, 0, 10)
    text_surface = FONT.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

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
    
    # Check if the clicked tile is adjacent to the blank space
    
    # Blank (r, c) coordinates
    r_blank, c_blank = blank_index // GRID_SIZE, blank_index % GRID_SIZE
    
    # Calculate distance
    dr = abs(r1 - r_blank)
    dc = abs(c1 - c_blank)
    
    # If adjacent (one distance unit, not diagonal)
    if (dr == 1 and dc == 0) or (dr == 0 and dc == 1):
        # Perform the swap
        board_list[current_index], board_list[blank_index] = \
            board_list[blank_index], board_list[current_index]
        return tuple(board_list)
        
    return board # No change

def shuffle_board():
    """Generates a random, guaranteed solvable board."""
    while True:
        temp_list = [i for i in range(9)]
        random.shuffle(temp_list)
        temp_board = tuple(temp_list)
        if is_solvable(temp_board):
            return temp_board

def solve_and_prepare_path(board):
    """Triggers the A* solver and stores the solution path."""
    print("Solver initiated...")
    solution_states, _ = solve_puzzle(board, manhattan_distance)
    
    if solution_states == "Unsolvable":
        print("Board is unsolvable!")
        return None
    elif solution_states:
        print(f"Solution found in {len(solution_states) - 1} moves.")
        return solution_states
    return None

# --- Main Game Loop ---
def main():
    global current_board_tuple, solving, solving_path, path_index
    clock = pygame.time.Clock()
    
    # Start with a randomly shuffled, solvable board
    current_board_tuple = shuffle_board()

    while True:
        SCREEN.fill(WHITE)
        
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                
                # 1. Tile Click (Only if not solving)
                if not solving and BOARD_RECT.collidepoint(pos):
                    r, c = get_clicked_tile(pos)
                    if r is not None:
                        current_board_tuple = slide_tile(current_board_tuple, r, c)
                        # Check for instant win
                        if current_board_tuple == GOAL_STATE:
                            print("Puzzle Solved Manually!")
                            solving = False # Stop any background solving
                            
                # 2. Button Clicks
                elif SOLVE_BUTTON_RECT.collidepoint(pos):
                    # Start solving process
                    solving_path = solve_and_prepare_path(current_board_tuple)
                    if solving_path:
                        solving = True
                        path_index = 0
                
                elif SHUFFLE_BUTTON_RECT.collidepoint(pos):
                    # Reset/Shuffle the board
                    solving = False
                    solving_path = None
                    path_index = 0
                    current_board_tuple = shuffle_board()
        
        # --- Solving/Animation Logic ---
        if solving and solving_path:
            # Slow down the animation using the clock timer
            if path_index < len(solving_path):
                # Animate the move every 300ms (adjust for speed)
                if pygame.time.get_ticks() % 300 < 50: 
                    current_board_tuple = solving_path[path_index].board
                    path_index += 1
            else:
                solving = False # Finished the animation
                print("Solution Animation Complete!")

        # --- Drawing ---
        draw_board(SCREEN, current_board_tuple)
        
        draw_button(SCREEN, SOLVE_BUTTON_RECT, "SOLVE (A*)", GREEN)
        draw_button(SCREEN, SHUFFLE_BUTTON_RECT, "SHUFFLE", DARK_GRAY)
        
        # Display status message
        if current_board_tuple == GOAL_STATE:
            status_text = FONT.render("SOLVED!", True, GREEN)
        elif solving:
             status_text = FONT.render(f"Solving... Move {path_index}/{len(solving_path)-1}", True, BLACK)
        else:
            status_text = FONT.render("Ready to Play or Solve", True, BLACK)

        status_rect = status_text.get_rect(center=(WIDTH // 2, HEIGHT - 20))
        SCREEN.blit(status_text, status_rect)
        
        pygame.display.flip()
        clock.tick(60) # 60 FPS

if __name__ == '__main__':
    # Add a check to ensure the solver module is accessible
    try:
        if not is_solvable(GOAL_STATE): # Basic check to ensure import success
            print("Error: Could not import core solver logic.")
            sys.exit()
    except Exception as e:
        print(f"FATAL: Ensure your 'solver.py' file is in the same directory.")
        print(f"Error details: {e}")
        sys.exit()

    main()
