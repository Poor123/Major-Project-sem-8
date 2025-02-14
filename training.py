import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments
from datasets import load_dataset

# Load the tokenizer and model
model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Load dataset from CSV
dataset = load_dataset("csv", data_files={
    "train": r"C:\Users\B15\Major-Project-sem-8\nlp_sql_dataset_vague.csv",
    "validation": r"C:\Users\B15\Major-Project-sem-8\nlp_sql_dataset_validation.csv"  # Added validation dataset
})

# Debug: Print column names
print("Dataset Columns:", dataset["train"].column_names)

# Ensure correct column names
expected_columns = {"NLP Query", "SQL Query"}
if not expected_columns.issubset(set(dataset["train"].column_names)):
    raise ValueError(f"Dataset does not have expected columns {expected_columns}. Found: {dataset['train'].column_names}")

# Tokenization function
def preprocess_data(example):
    inputs = tokenizer("translate English to SQL: " + example["NLP Query"], padding="max_length", truncation=True, max_length=128)
    targets = tokenizer(example["SQL Query"], padding="max_length", truncation=True, max_length=128)
    
    inputs["labels"] = targets["input_ids"]
    return inputs

# Apply tokenization
dataset = dataset.map(preprocess_data)

# Set training arguments
training_args = TrainingArguments(
    output_dir="./t5_finetuned_sql",
    per_device_train_batch_size=8,
    num_train_epochs=3,
    logging_dir="./logs",
    logging_steps=10,
    save_total_limit=2,
    save_strategy="epoch",
    eval_strategy="epoch",  # Updated from evaluation_strategy (deprecated)
    learning_rate=3e-5,
    weight_decay=0.01,
    warmup_steps=500
)

# Trainer initialization
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["validation"]  # Added evaluation dataset
)

# Train the model
trainer.train()

# Save the fine-tuned model
model.save_pretrained("./t5_sql_model")
tokenizer.save_pretrained("./t5_sql_model")

print("Training complete! Model saved in 't5_sql_model' folder.")