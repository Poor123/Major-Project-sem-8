import pandas as pd
from difflib import SequenceMatcher

# Load the test output dataset (model-generated)
test_output_path = r"C:\Users\B15\Major-Project-sem-8\nlp_sql_predictions.csv"  # Update path
df_test_output = pd.read_csv(test_output_path)

# Load the ground truth dataset (correct answers)
ground_truth_path = "path/to/nlp_sql_dataset_vague.csv"  # Update path
df_ground_truth = pd.read_csv(ground_truth_path)

# Merge datasets on NLP Query (ensure correct mapping)
df_merged = df_test_output.merge(df_ground_truth, on="NLP Query", suffixes=("_pred", "_true"))

# Function to calculate string similarity (SQL Query comparison)
def similarity(a, b):
    return SequenceMatcher(None, str(a), str(b)).ratio()

# Compute accuracy metrics
df_merged["SQL Similarity"] = df_merged.apply(lambda row: similarity(row["SQL Query_pred"], row["SQL Query_true"]), axis=1)
df_merged["Visualization Match"] = df_merged["Recommended Visualization_pred"] == df_merged["Recommended Visualization_true"]

# Compute overall accuracy
sql_accuracy = df_merged["SQL Similarity"].mean() * 100  # Avg similarity in percentage
vis_accuracy = df_merged["Visualization Match"].mean() * 100  # Percentage of correct matches

print(f"SQL Query Accuracy: {sql_accuracy:.2f}%")
print(f"Visualization Recommendation Accuracy: {vis_accuracy:.2f}%")
