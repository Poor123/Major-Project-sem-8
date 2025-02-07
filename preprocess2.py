import pandas as pd
import numpy as np
import re
import os

# Define file paths
file_path = r"C:\Users\PC-05\Desktop\NLP2VIZ\extracurr dataset.xlsx"  
output_path = r"C:\Users\PC-05\Desktop\NLP2VIZ\preprocessed_extracurr.csv"  

# Ensure the file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Error: File not found at {file_path}")

# Load Excel file and check available sheet names
xls = pd.ExcelFile(file_path)
print("Available sheets:", xls.sheet_names)  # Debugging step

# Select the correct sheet name (update manually if needed)
sheet_name = xls.sheet_names[0]  # Automatically picks the first sheet
df = pd.read_excel(xls, sheet_name=sheet_name)

# Convert all text to lowercase (only if the column exists)
df = df.applymap(lambda x: x.lower() if isinstance(x, str) else x)

# Remove punctuation and special characters from text columns
def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', text) if isinstance(text, str) else text

text_columns = ["Name", "activity"]
for col in text_columns:
    if col in df.columns:
        df[col] = df[col].apply(remove_punctuation)

# Standardize date format (extract year if applicable)
def extract_year(year_str):
    return re.sub(r'(\d{4})-(\d{4})', r'\1', year_str) if isinstance(year_str, str) else year_str

if "year" in df.columns:
    df["year"] = df["year"].apply(extract_year)

# Handle missing values in numerical columns (fill with mean if they exist)
numeric_columns = ["score", "hours"]
for col in numeric_columns:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].mean())

# Normalize numerical values (Min-Max Scaling)
for col in numeric_columns:
    if col in df.columns:
        df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min()) if df[col].max() != df[col].min() else df[col]

# Encode categorical variables (activity column if applicable)
if "activity" in df.columns and df["activity"].dtype == object:
    activity_mapping = {activity: idx for idx, activity in enumerate(df["activity"].dropna().unique())}
    df["activity"] = df["activity"].map(activity_mapping)

# Ensure output directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save the preprocessed dataset
df.to_csv(output_path, index=False)

# Display first few rows of the cleaned dataset
print(df.head())
