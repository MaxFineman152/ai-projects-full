# Knights and Knaves Logic Solver

A propositional logic solver that determines which characters are knights (always tell the truth) or knaves (always lie) using model checking.

---

## Overview
Models classic Knights and Knaves puzzles using logical sentences and checks which assignments of truth values satisfy each puzzle.

---

## Features
- Symbolic logic representation (AND, OR, NOT, IMPLICATION, BICONDITIONAL)  
- Model checking via exhaustive truth assignment  
- Solves multiple Knights and Knaves puzzles  
- Encodes statements as logical constraints  
- Automatically deduces valid knight/knave identities  

---

## Technologies
- Python  
- Custom propositional logic engine  
- Recursive model checking algorithm  
- Set-based symbol evaluation  

---

## Puzzles
- Puzzle 0–3 encoded as logical knowledge bases  
- Each character is either:
  - Knight (truth-teller)  
  - Knave (liar)  

---

## Output
- Prints which symbols (A, B, C as Knight/Knave) are logically entailed  
- Fully consistent solutions for each puzzle  
