import pandas as pd
import os

# Load the dataset
file_path = r"C:\Users\B15\Major-Project-sem-8\result dataset.xlsx"  # Update with the correct path
output_folder = "processed_data"   # Folder to store cleaned files

# Create output directory if not exists
os.makedirs(output_folder, exist_ok=True)

# Read the Excel file
df = pd.read_excel(file_path)

# Convert 'gpa' to numeric, setting errors='coerce' to handle invalid values
df["gpa"] = pd.to_numeric(df["gpa"], errors="coerce")

# Fill missing GPA values with the median (ensuring it's correctly applied)
median_gpa = df["gpa"].median()
df["gpa"].fillna(median_gpa, inplace=True)

# Fill missing result values with the mode
if not df["result"].isna().all():
    df["result"].fillna(df["result"].mode()[0], inplace=True)

# Remove duplicates
df.drop_duplicates(inplace=True)

# Convert 'result' column to numeric: 'P' -> 1, 'F' -> 0
df["result"] = df["result"].map({"P": 1, "F": 0})

# Remove outliers in 'gpa' (valid range 0-10)
df = df[(df["gpa"] >= 0) & (df["gpa"] <= 10)]

# Identify date columns and convert them to standard format (YYYY-MM-DD)
for col in df.select_dtypes(include=["object"]):  # Check string columns
    try:
        df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%Y-%m-%d")
    except:
        continue  # Skip non-date columns

# Remove rows with completely invalid dates (NaT)
df.dropna(subset=[col for col in df.columns if "date" in col.lower()], inplace=True)

# Save cleaned dataset as Excel and CSV
excel_output = os.path.join(output_folder, "preprocessed_dataset.xlsx")
csv_output = os.path.join(output_folder, "preprocessed_dataset.csv")

df.to_excel(excel_output, index=False)
df.to_csv(csv_output, index=False)

print("Preprocessing complete!")
print(f"Cleaned dataset saved as:\n - {excel_output}\n - {csv_output}")
