import torch
import pandas as pd
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the fine-tuned model and tokenizer
model_path = "./t5_sql_vis_model"
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)

# Load the test CSV file
test_file_path = r"C:\Users\B15\Major-Project-sem-8\nlp_sql_dataset_test.csv"
df = pd.read_csv(test_file_path)

# Ensure expected columns exist
expected_columns = {"NLP Query", "SQL Query", "Recommended Visualization"}
if not expected_columns.issubset(set(df.columns)):
    raise ValueError(f"Dataset does not have expected columns {expected_columns}. Found: {df.columns}")

# Generate SQL Queries and Recommended Visualizations
def generate_sql_and_visualization(nlp_query):
    input_text = "translate English to SQL and visualization: " + nlp_query
    input_ids = tokenizer(input_text, return_tensors="pt", padding="max_length", truncation=True, max_length=128).input_ids
    
    # Generate output
    with torch.no_grad():
        output_ids = model.generate(input_ids, max_length=128)
    
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    
    # Splitting SQL query and visualization
    if "Recommended Visualization:" in output_text:
        sql_query, visualization = output_text.split("Recommended Visualization:")
        sql_query = sql_query.strip()
        visualization = visualization.strip()
    else:
        sql_query = output_text.strip()
        visualization = ""
    
    return sql_query, visualization

# Apply generation to all rows
df["SQL Query"], df["Recommended Visualization"] = zip(*df["NLP Query"].apply(generate_sql_and_visualization))

# Save the results to a new CSV file
output_file_path = "C:/Users/B15/Major-Project-sem-8/nlp_sql_predictions.csv"
df.to_csv(output_file_path, index=False)

print(f"✅ Predictions saved to {output_file_path}")
