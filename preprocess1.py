import pandas as pd
import numpy as np
import re

file_path = r"C:\Users\PC-05\Desktop\NLP2VIZ\acad prog dataset.xlsx"  # Update this path if needed
xls = pd.ExcelFile(file_path)
df = pd.read_excel(xls, sheet_name="acad prog")

# Convert all text to lowercase
df = df.applymap(lambda x: x.lower() if isinstance(x, str) else x)

# Remove punctuation and special characters from text columns
def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', text) if isinstance(text, str) else text

df["Name"] = df["Name"].apply(remove_punctuation)
df["stat"] = df["stat"].apply(remove_punctuation)

# Standardize academic year format (convert "2011-2012" to "2011")
def extract_year(year_str):
    return re.sub(r'(\d{4})-(\d{4})', r'\1', year_str) if isinstance(year_str, str) else year_str

df["acadyear"] = df["acadyear"].apply(extract_year)

# Handle missing values in numerical columns (fill with mean)
num_cols = ["ssc", "hsc", "cet", "diploma"]
df[num_cols] = df[num_cols].apply(lambda x: x.fillna(x.mean()))

# Normalize numerical values (Min-Max Scaling)
df[num_cols] = (df[num_cols] - df[num_cols].min()) / (df[num_cols].max() - df[num_cols].min())

# Encode categorical variables (status column)
status_mapping = {status: idx for idx, status in enumerate(df["stat"].unique())}
df["stat"] = df["stat"].map(status_mapping)

# Save the preprocessed dataset
df.to_csv("preprocessed_acad_prog.csv", index=False)

# Display first few rows of the cleaned dataset
print(df.head())