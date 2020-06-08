import torch
import math
import operator

from transformers import BertForQuestionAnswering
from transformers import BertTokenizer

def _compute_softmax(scores):
    """Compute softmax probability over raw logits."""
    max_score = None
    for score in scores:
        if max_score is None or score > max_score:
            max_score = score

    exp_scores = []
    total_sum = 0.0
    for score in scores:
        x = math.exp(score - max_score)
        exp_scores.append(x)
        total_sum += x

    probs = []
    for score in exp_scores:
        probs.append(score / total_sum)
        
    return max(probs)


model_name = 'bert-large-uncased-whole-word-masking-finetuned-squad'
model = BertForQuestionAnswering.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)

question = "who is ceo of netcetera?"

with open('domain-content.txt', 'r') as answer_file:
    domain_text = answer_file.read()

source_texts = domain_text.split('\n\n')

answers = {}

for text in source_texts:
    if len(text) > 1000:
        text = text[:1000]
    
    input_text = "[CLS] " + question + " [SEP] " + text + " [SEP]"
    input_ids = tokenizer.encode(input_text)

    token_type_ids = [0 if i <= input_ids.index(102) else 1 for i in range(len(input_ids))] 
    start_scores, end_scores = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([token_type_ids]))

    all_tokens = tokenizer.convert_ids_to_tokens(input_ids)  
    answer = ' '.join(all_tokens[torch.argmax(start_scores) : torch.argmax(end_scores)+1])

    if len(answer) == 0 or answer == '[CLS]':
        continue

    # prob = _compute_softmax(start_scores[0] + end_scores[0])
    prob = _compute_softmax(start_scores[0])

    if prob < 0.5:
        continue
    
    answer = answer.replace(" ##", "")
    print("prob: " + str(prob) + "; answer: " + answer)
    answers[answer] = prob

answers = dict(sorted(answers.items(), key=operator.itemgetter(1),reverse=True))

from itertools import islice
print("len: " + str(len(answers)))
if len(answers) > 10:
    answers = dict(islice(answers.items(), 10))
for answer, prob in answers.items(): 
    print(str(prob) + " : " + answer)