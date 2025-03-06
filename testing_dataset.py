import pandas as pd

# Load your existing training dataset
dataset_path = r"C:\Users\Admin\Downloads\Major-Project-sem-8-main\Major-Project-sem-8-main\nlp_sql_dataset_vague.csv"  # Update with your correct path
df_train = pd.read_csv(dataset_path)

# Ensure the dataset has an 'NLP Query' column
if "NLP Query" not in df_train.columns:
    raise ValueError("Dataset must have an 'NLP Query' column.")

# Generate a test dataset with 2000 NLP queries
test_queries = df_train["NLP Query"].tolist()

# If the dataset has fewer than 2000 unique queries, repeat entries
while len(test_queries) < 2000:
    test_queries.extend(test_queries[:2000 - len(test_queries)])

# Create a new DataFrame for testing
df_test = pd.DataFrame({"NLP Query": test_queries[:2000]})

# Save test dataset as CSV
df_test.to_csv("test_nlp_queries.csv", index=False)

print("Test dataset created: test_nlp_queries.csv")
