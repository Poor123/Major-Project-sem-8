from transformers import T5Tokenizer

# Load T5 tokenizer
tokenizer = T5Tokenizer.from_pretrained("t5-small")

# Tokenize the dataset
train_encodings = tokenizer(train_texts, padding=True, truncation=True, return_tensors="pt")
val_encodings = tokenizer(val_texts, padding=True, truncation=True, return_tensors="pt")

train_labels = tokenizer(train_targets, padding=True, truncation=True, return_tensors="pt")
val_labels = tokenizer(val_targets, padding=True, truncation=True, return_tensors="pt")
