import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the fine-tuned model and tokenizer
model_name = "./t5_sql_model"  # Path to your saved model
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def generate_sql(nlp_query):
    """Function to generate SQL query from an NLP query."""
    # Tokenize input query
    input_text = "translate English to SQL: " + nlp_query
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=128)

    # Generate output
    with torch.no_grad():
        output = model.generate(**inputs, max_length=128)

    # Decode generated SQL query
    sql_query = tokenizer.decode(output[0], skip_special_tokens=True)
    return sql_query

# Example test queries
test_queries = [
    "Show me all students who have gpa below 8",
    "List the names of students whose hobby is playing badminton at state level",
    "Show me students who have scored less percentage in hsc exam."
]

# Run the test queries
for query in test_queries:
    sql_result = generate_sql(query)
    print(f"NLP Query: {query}\nGenerated SQL: {sql_result}\n")
