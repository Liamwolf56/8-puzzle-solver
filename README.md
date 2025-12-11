# 🧩 High-Performance 8-Puzzle Solver (A* with Pattern Databases)

This project is an interactive 8-Puzzle solver built using Python and Pygame. It utilizes the **A\* Search Algorithm** guided by an optimized **Pattern Database (PDB)** heuristic, allowing it to find the optimal solution (shortest path) for any solvable 8-puzzle configuration almost instantaneously.

## ✨ Key Features & Technical Achievements

* **Optimal A\* Search:** Guarantees the shortest sequence of moves to solve the puzzle.
* **Pattern Database (PDB) Heuristic:** Implements a 6-tile PDB, which provides the most informed estimate of remaining cost, resulting in a dramatic reduction of the search space compared to standard heuristics.
    * **Performance:** Solves complex puzzles with **tens of thousands of nodes explored** using Manhattan Distance in a matter of milliseconds by exploring fewer than **100 nodes** with the PDB.
* **Solvability Check:** Mathematically verifies the solvability of any randomly generated or user-inputted board state before initiating the search.
* **Interactive GUI:** A user-friendly graphical interface built with Pygame for manual play, quick shuffling, and step-by-step visualization of the optimal solution path.

## 🚀 Getting Started

### Prerequisites

You need Python 3 and the `pygame` library installed.

```bash
pip install pygame
