import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the fine-tuned model
model_path = "./t5_sql_model"
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)

# Function to generate SQL from NLP query
def generate_sql(nlp_query):
    input_text = "translate English to SQL: " + nlp_query
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=128)

    # Generate SQL output
    with torch.no_grad():
        outputs = model.generate(**inputs)

    sql_query = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return sql_query

# Test queries
test_queries = [
    "Show me all students who have gpa below 8",
    "List the names of students whose hobby is playing badminton at state level",
    "Show me students who have scored less percentage in hsc exam."
]

# Generate predictions
predicted_sql_queries = [generate_sql(query) for query in test_queries]

# Print results
for i, query in enumerate(test_queries):
    print(f"NLP Query: {query}")
    print(f"Generated SQL: {predicted_sql_queries[i]}")
    print("-" * 50)
