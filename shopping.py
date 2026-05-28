import csv
import sys
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    file = pd.read_csv(filename)
    length = len(file)

    month_dict = {"Jan": 0,
                  "Feb": 1,
                  "Mar": 2,
                  "Apr": 3,
                  "May": 4,
                  "June": 5,
                  "Jul": 6,
                  "Aug": 7,
                  "Sep": 8,
                  "Oct": 9,
                  "Nov": 10,
                  "Dec": 11,
                  }
    file["Month"] = file["Month"].replace(to_replace=month_dict)  # Convert months to int

    weekend_dict = {False: 0,
                    True: 1
                    }
    file["Weekend"] = file["Weekend"].replace(to_replace=weekend_dict)  # Weekend to int

    returning_dict = {"Returning_Visitor": 1,
                      "New_Visitor": 0,
                      "Other": 0
                      }
    file["VisitorType"] = file["VisitorType"].replace(
        to_replace=returning_dict)  # Visitor type to int

    revenue_dict = {"FALSE": 0,
                    "TRUE": 1
                    }
    file["Revenue"] = file["Revenue"].replace(to_replace=revenue_dict)  # Revenue to int

    labels = []
    evidence = []

    # Group data into labeled evidence values
    evidence_df = file.drop(labels="Revenue", axis=1)
    for row in range(length):
        evidence_row = evidence_df.loc[row].values.tolist()
        evidence.append(evidence_row)
        labels_row = file.loc[row, "Revenue"]
        labels.append(labels_row)

    # Convert out of numpy
    for list in evidence:
        for i, item in enumerate(list):
            if isinstance(item, np.integer):
                list[i] = int(item)
            if isinstance(item, np.float64):
                list[i] = float(item)

    return (evidence, labels)
    

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    neigh = KNeighborsClassifier(n_neighbors=1)  # Generate k-nearest neighbor model
    return neigh.fit(evidence, labels)  # Fit using model
    

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # Check each user is predicted for
    if len(labels) != len(predictions):
        raise Exception("Labels and Predictions not same length")
    
    # Initialise values
    true_positives = 0
    true_negatives = 0
    total_positives = 0
    total_negatives = 0
    
    for label, prediction in zip(labels, predictions):
        # Sum expected and actual positive results
        if label == 1:
            if label == prediction:
                true_positives += 1
                total_positives += 1
            else:
                total_positives += 1
        
        # Sum expected and actual negative results
        if label == 0:
            if label == prediction:
                true_negatives += 1
                total_negatives += 1
            else:
                total_negatives += 1
    
    # Calculations
    sensitivity = true_positives / total_positives
    specificity = true_negatives / total_negatives

    return (sensitivity, specificity)
            

if __name__ == "__main__":
    main()
