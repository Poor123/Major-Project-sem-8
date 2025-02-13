import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments
from datasets import load_dataset

# Load the tokenizer and model
model_name = "t5-small"  # Change to "t5-base" or "t5-large" if needed
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Load dataset
dataset_path = r"C:\Users\B15\Major-Project-sem-8\nlp_sql_dataset_vague.csv"
dataset = load_dataset("csv", data_files={"train": dataset_path})

# Verify column names
print("Dataset columns:", dataset["train"].column_names)

# Ensure the correct column names are used
if "NLP Query" not in dataset["train"].column_names or "SQL Query" not in dataset["train"].column_names:
    raise ValueError("Dataset must have columns 'NLP Query' and 'SQL Query'. Found: " + str(dataset["train"].column_names))

# Tokenization function
def preprocess_data(example):
    if isinstance(example["NLP Query"], str) and isinstance(example["SQL Query"], str):
        input_text = "translate English to SQL: " + example["NLP Query"]
        target_text = example["SQL Query"]
        
        # Tokenization
        inputs = tokenizer(input_text, padding="max_length", truncation=True, max_length=128, return_tensors="pt")
        targets = tokenizer(target_text, padding="max_length", truncation=True, max_length=128, return_tensors="pt")

        # Convert to standard format and replace padding token (-100 is used to ignore loss computation on padding tokens)
        inputs = {key: val.squeeze(0) for key, val in inputs.items()}
        targets = {key: val.squeeze(0) for key, val in targets.items()}
        inputs["labels"] = targets["input_ids"]
        inputs["labels"][inputs["labels"] == tokenizer.pad_token_id] = -100  # Ensure padding tokens are ignored in loss calculation

        return inputs
    else:
        return {}

# Apply tokenization (batch processing)
dataset = dataset.map(preprocess_data, batched=True, remove_columns=["NLP Query", "SQL Query"])

# Convert dataset to PyTorch format
dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])

# Set training arguments
training_args = TrainingArguments(
    output_dir="./t5_finetuned_sql",
    per_device_train_batch_size=8,
    num_train_epochs=3,
    logging_dir="./logs",
    logging_steps=10,
    save_total_limit=2,
    save_strategy="epoch",
    evaluation_strategy="epoch",
    learning_rate=3e-5,
    weight_decay=0.01,
    warmup_steps=500,
    report_to="none"  # Disable logging to external services
)

# Trainer initialization
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"]
)

# Train the model
trainer.train()

# Save the fine-tuned model
model.save_pretrained("./t5_sql_model")
tokenizer.save_pretrained("./t5_sql_model")

print("Training complete! Model saved in 't5_sql_model' folder.")
