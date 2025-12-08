# 🧩 8-Puzzle Solver using A* Search

This project implements a solver for the classic 8-Puzzle (a 3x3 sliding tile puzzle) using the **A* Search Algorithm**, a classic best-first search method often used in graph traversal and pathfinding problems.

## 🚀 Getting Started

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Liamwolf56/8-puzzle-solver.git](https://github.com/Liamwolf56/8-puzzle-solver.git)
    cd 8-puzzle-solver
    ```
2.  **Activate environment (WSL/Linux):**
    ```bash
    source venv/bin/activate
    ```
3.  **Run the solver:**
    ```bash
    python3 solver.py
    ```

## 🧠 Algorithm & Heuristics

The solver uses the A* algorithm, which finds the shortest path by minimizing the total estimated cost $f(n)$.

### Cost Function (A*)
The cost function is defined as: $f(n) = g(n) + h(n)$, where:
* **$g(n)$**: The actual number of moves taken from the start state to the current state $n$.
* **$h(n)$**: The heuristic estimate of the distance from the current state $n$ to the goal state.

### Heuristic: Manhattan Distance
This implementation utilizes the **Manhattan Distance** ($h(n)$) as the heuristic. 
Manhattan Distance is calculated as the sum of the horizontal and vertical distances of each misplaced tile from its position in the goal state. This is an **admissible heuristic**, meaning it never overestimates the true cost, thus guaranteeing the A* algorithm finds the optimal (shortest) solution.

## 📊 Complexity Analysis

The time complexity of the A* search algorithm is difficult to state precisely without knowing the quality of the heuristic. However, in general terms, the complexity is:

$$O(b^d)$$

Where:
* $b$ is the **branching factor** (for the 8-puzzle, $b \approx 2$ to $3$).
* $d$ is the **depth** of the solution (the number of moves in the shortest path).

For the 8-Puzzle, the Manhattan Distance heuristic dramatically reduces the search space compared to an uninformed search (like Breadth-First Search).

## ✅ Advanced Feature: Solvability Check

Not all random initial states of the 8-Puzzle are solvable. The solver first checks the initial board configuration using the **Inversion Count** method.

### Inversion Count Rule
For an N-Puzzle with an **odd grid width** (like the 3x3 8-puzzle), the puzzle is solvable if and only if the number of inversions is **even**.

If the puzzle is detected as unsolvable, the A* search is skipped immediately, preventing the program from wasting resources on an impossible problem.
