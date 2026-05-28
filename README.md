# Degrees of Separation (IMDb Graph Search)

A breadth-first search (BFS) program that finds the shortest connection between two actors based on shared movie appearances.

---

## Overview
Builds a graph of actors and movies from IMDb-style datasets and uses BFS to find the shortest path (degrees of separation) between two people.

---

## Features
- Loads people, movies, and cast data from CSV files  
- Resolves ambiguous actor names  
- Builds an implicit graph of actors connected via shared movies  
- Finds shortest path using BFS  
- Outputs step-by-step connection chain  
- Handles large datasets efficiently  

---

## Technologies
- Python  
- CSV module  
- Queue-based BFS (frontier system)  
- Custom graph node structure  

---

## Input Data
- `people.csv` — actor IDs, names, birth years  
- `movies.csv` — movie IDs, titles, years  
- `stars.csv` — links between actors and movies  

---

## Output
- Degree of separation between two actors  
- Step-by-step path showing:
  - Actor A → Actor B  
  - Movie they appeared in together  
