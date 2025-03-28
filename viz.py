import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="NewPassword",
    database="student_db"
)
cursor = conn.cursor()

# Get user input for NLP Query
nlp_query = input("Enter your NLP Query: ")

# Retrieve SQL query and visualization type from model_output table
cursor.execute("SELECT sql_query, recommended_visualization FROM model_output WHERE nlp_query = %s", (nlp_query,))
result = cursor.fetchone()
cursor.fetchall()

if result:
    sql_query, visualization_type = result
    
    # Fetch data from the database
    df = pd.read_sql(sql_query, conn)
    
    # Generate random colors
    colors = ["#" + ''.join(random.choices('0123456789ABCDEF', k=6)) for _ in range(len(df))]
    
    # Generate visualization
    if visualization_type.lower() == "bar chart":
        ax = df.plot(kind='bar', x=df.columns[0], y=df.columns[1], legend=False, color=colors)
        plt.xlabel(df.columns[0])
        plt.ylabel("Count")
        plt.title(nlp_query)
        plt.xticks(rotation=45)
        
        # Add annotations
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.1f}', (p.get_x() + p.get_width() / 2, p.get_height()),
                        ha='center', va='bottom', fontsize=10, color='black')
        plt.show()

    elif visualization_type.lower() == "pie chart":
        ax = df.set_index(df.columns[0]).plot(kind='pie', y=df.columns[1], autopct='%1.1f%%',
                                               legend=False, colors=colors)
        plt.ylabel('')
        plt.title(nlp_query)
        plt.show()
    
    else:
        print(f"Visualization type '{visualization_type}' is not supported.")
else:
    print("No matching NLP query found in model_output table.")

# Close database connection
cursor.close()
conn.close()
