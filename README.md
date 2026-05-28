# Attention Scores

A BERT-based model that predicts masked words and visualises self-attention weights.

---

## Overview
Uses a pre-trained `bert-base-uncased` model to predict masked tokens and extract attention weights for visualisation.

---

## Features
- Masked word prediction using BERT  
- Top-K predictions for `[MASK]` token  
- Extraction of attention weights  
- Visualisation of attention per layer and head  
- Saves attention heatmaps as images  

---

## Technologies
- Python  
- TensorFlow  
- PyTorch (Transformers)  
- Hugging Face Transformers  
- Pillow  
- NumPy  

---

## Output
- Predicted masked words  
- Attention heatmaps saved per layer and head
