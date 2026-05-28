# Heredity Inference Model

A probabilistic model that computes gene and trait probabilities for individuals in a family using Bayesian inference.

---

## Overview
Estimates the likelihood of each person having 0, 1, or 2 copies of a gene, and whether they express a trait, based on family relationships and observed data.

---

## Features
- Models gene inheritance with mutation probability  
- Computes trait probability from gene count  
- Handles parent-child relationships  
- Evaluates all possible gene/trait combinations  
- Uses joint probability aggregation  
- Normalizes final probability distributions  

---

## Technologies
- Python  
- CSV processing  
- Itertools (powerset generation)  
- Bayesian probability modeling  

---

## Input
CSV file with:
- names  
- mother / father  
- optional trait values  

---

## Output
For each person:
- Probability of 0, 1, or 2 gene copies  
- Probability of trait (True/False)  
- Normalized probability distributions  
