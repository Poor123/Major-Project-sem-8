import pandas as pd
import mysql.connector

# Load the dataset
file_path = r"C:\Users\Admin\Downloads\college_students_dataset_unique_names.csv"
df = pd.read_csv(file_path)

# Select the first 150 entries
df = df.head(150)

# Print dataset preview to verify it's loaded correctly
print("\U0001F4CA Preview of dataset:")
print(df.head())

# Ensure 'pid' is unique and starts from 197882
df['pid'] = range(197882, 197882 + len(df))

# Handle missing values by filling them with defaults
df = df.fillna({'diploma': 0, 'cet': 0})

# Ensure column data types match MySQL schema
df['sem'] = df['sem'].astype(float)
df['gpa'] = df['gpa'].astype(str)

df_tuples = [tuple(row) for row in df.itertuples(index=False, name=None)]

# MySQL connection details - Update these accordingly
DB_CONFIG = {
    "host": "localhost",  # Change if MySQL is on another host
    "user": "root",  # Change to your MySQL username
    "password": "NewPassword",  # Change to your MySQL password
    "database": "student_db"  # Change to your database name
}

try:
    # Connect to MySQL
    db_conn = mysql.connector.connect(**DB_CONFIG)
    cursor = db_conn.cursor()
    print("✅ Successfully connected to the database.")
    
    # Define insert query
    insert_query = '''
        INSERT INTO SFIT_students (pid, sem, month_year, gpa, result, ECategory, Hobby, Hobby_level, 
                                  Name, acadyear, stat, ssc, hsc, cet, diploma)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    
    # Insert data into MySQL table
    cursor.executemany(insert_query, df_tuples)
    db_conn.commit()
    print(f"✅ {cursor.rowcount} rows inserted into the 'SFIT_students' table.")

except mysql.connector.Error as err:
    print(f"❌ Database Error: {err}")

except Exception as err:
    print(f"❌ Unexpected Error: {err}")

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'db_conn' in locals():
        db_conn.close()
    print("🔒 Database connection closed.")