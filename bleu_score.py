from nltk.translate.bleu_score import sentence_bleu

def compute_bleu_score(predictions, ground_truths):
    scores = [sentence_bleu([gt.split()], pred.split()) for pred, gt in zip(predictions, ground_truths)]
    return sum(scores) / len(scores)

bleu_score = compute_bleu_score(predicted_sql_queries, correct_sql_queries)
print(f"BLEU Score: {bleu_score:.2f}")
