# Crossword Puzzle Generator

A CSP-based crossword solver using backtracking search and constraint propagation to fill a grid from a word list.

---

## Overview
Solves crossword puzzles by treating each word slot as a variable in a constraint satisfaction problem, enforcing word constraints and overlaps.

---

## Features
- Detects across and down word slots from a grid structure  
- Node consistency (word length filtering)  
- Arc consistency using AC-3  
- Backtracking search solver  
- MRV + degree heuristic for variable selection  
- Least-constraining-value ordering  
- Terminal and image output  

---

## Technologies
- Python  
- Pillow (PIL) for image rendering  
- CSP algorithms (AC-3, backtracking)  

---

## Output
- Completed crossword in terminal  
- Optional saved image of solved grid  
- Full variable-to-word assignment solution  
