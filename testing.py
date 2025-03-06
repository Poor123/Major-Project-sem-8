import torch
import sqlite3
import pandas as pd
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the fine-tuned T5 model
model_name = ""  # Ensure this is your saved fine-tuned model path
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Connect to database (Replace with actual database if needed)
conn = sqlite3.connect("student_data.db")  

# Load test dataset (2000 NLP queries)
test_file = r"C:\Users\Admin\Downloads\Major-Project-sem-8-main\test_nlp_queries.csv"  # Ensure this file is present in the working directory
df_test = pd.read_csv(test_file)  

# Ensure column exists
if "NLP Query" not in df_test.columns:
    raise ValueError("CSV file must have a column named 'NLP Query'.")

def generate_sql(nlp_query):
    """Generates an SQL query from an NLP query using the fine-tuned T5 model."""
    input_text = "translate English NLP to English SQL: " + nlp_query
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    output_ids = model.generate(input_ids)
    sql_query = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    
    return sql_query

def recommend_chart_type(sql_query):
    """Suggests a chart type based on SQL query structure."""
    sql_query_lower = sql_query.lower()

    if "group by" in sql_query_lower:
        return "Bar Chart"  # Suitable for category comparisons
    elif "count(" in sql_query_lower or "sum(" in sql_query_lower:
        return "Pie Chart"  # Suitable for proportions
    else:
        return "Bar Chart"  # Default to bar

def test_nlp_to_sql():
    """Tests model on 2000 NLP queries from CSV."""
    results = []

    for index, row in df_test.iterrows():
        nlp_query = row["NLP Query"]
        sql_query = generate_sql(nlp_query)
        chart_type = recommend_chart_type(sql_query)

        print(f"\n🔹 NLP Query: {nlp_query}")
        print(f"🔹 Generated SQL Query: {sql_query}")
        print(f"🔹 Recommended Chart: {chart_type}")

        # Try executing SQL (only if the database is properly set up)
        try:
            df_result = pd.read_sql_query(sql_query, conn)
            print("🔹 Query Output (First 5 Rows):\n", df_result.head())
        except Exception as e:
            print("⚠️ Error executing SQL:", e)

        # Store results
        results.append({"NLP Query": nlp_query, "SQL Query": sql_query, "Chart Type": chart_type})

    # Save results to CSV for analysis
    results_df = pd.DataFrame(results)
    results_df.to_csv("sql_predictions.csv", index=False)
    print("\n✅ SQL Predictions saved in 'sql_predictions.csv'!")

# Run the test function
test_nlp_to_sql()
