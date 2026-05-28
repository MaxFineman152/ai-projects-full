# Shopping Revenue Predictor (Machine Learning)

A machine learning model that predicts whether a user will generate revenue from shopping session data.

---

## Overview
Uses a k-nearest neighbors classifier (k=1) to predict online shopping revenue based on user behavior and session features.

---

## Features
- Loads and preprocesses real-world shopping dataset  
- Encodes categorical variables (months, visitor type, weekend, revenue)  
- Splits data into training and testing sets  
- Trains a KNN classifier  
- Evaluates performance using sensitivity and specificity  

---

## Technologies
- Python  
- Pandas  
- NumPy  
- Scikit-learn (KNeighborsClassifier, train_test_split)  

---

## Input
CSV dataset containing user session features such as:
- Page visits and durations  
- Bounce/exit rates  
- Visitor type and region  
- Time-based features (month, weekend)  

---

## Output
- Predicted revenue outcomes (0 or 1)  
- Accuracy statistics:
  - Correct / incorrect predictions  
  - True positive rate (sensitivity)  
  - True negative rate (specificity)  
