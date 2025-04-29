import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load your dataset
df = pd.read_csv(r'C:\Users\Admin\Downloads\Remarks final dataset.csv')

# Define columns for actual and predicted queries
actual_col = 'Actual Queries'
predicted_col = 'Predicted Queries'

# Initialize TfidfVectorizer for logical match (cosine similarity)
vectorizer = TfidfVectorizer()

# Function to calculate cosine similarity between two queries
def calculate_cosine_similarity(query1, query2):
    # Transform queries into TF-IDF vectors
    tfidf_matrix = vectorizer.fit_transform([query1, query2])
    # Compute cosine similarity (cosine similarity between first and second query)
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return cosine_sim[0][0]

# Function to generate remarks
def generate_remarks(row):
    actual_query = row[actual_col]
    predicted_query = row[predicted_col]
    
    # Exact Match (strict case and content match)
    if actual_query.strip() == predicted_query.strip():
        return "Exactly Matched"
    
    # Logical Match (cosine similarity > threshold)
    cosine_sim = calculate_cosine_similarity(actual_query, predicted_query)
    threshold = 0.8  # Adjust threshold for logical match as needed
    if cosine_sim >= threshold:
        return "Logically Matched"
    
    # If neither match
    return "Not Matched"

# Apply the generate_remarks function to each row
df['Remarks'] = df.apply(generate_remarks, axis=1)

# Check current working directory
print(f"Current working directory: {os.getcwd()}")

# Save the updated dataframe with remarks to a new CSV file in Downloads folder
output_path = r'C:\Users\Admin\Downloads\Remarks_with_remarks.csv'
df.to_csv(output_path, index=False)

# Verify the output
print(f"File saved to: {output_path}")
print(df.head())
