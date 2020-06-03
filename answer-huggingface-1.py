import torch

from transformers import BertForQuestionAnswering
from transformers import BertTokenizer

# model_name = 'bert-large-uncased-whole-word-masking-finetuned-squad'
# model = BertForQuestionAnswering.from_pretrained(model_name)
# tokenizer = BertTokenizer.from_pretrained(model_name)

model_name = 'deepset/bert-large-uncased-whole-word-masking-squad2'
model = BertForQuestionAnswering.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)

question = "what is nets?"

with open('html\\20080130-sbb-nets.txt', 'r') as answer_file:
    answer_text = answer_file.read()

# answer_text = """BERT-large is really big... it has 24-layers and an embedding
# size of 1,024, for a total of 340M parameters! Altogether it is 1.34GB,
# so expect it to take a couple minutes to download to your Colab instance."""

# Apply the tokenizer to the input text, treating them as a text-pair.
input_ids = tokenizer.encode(question, answer_text)

# BERT only needs the token IDs, but for the purpose of inspecting the
# tokenizer's behavior, let's also get the token strings and display them.
tokens = tokenizer.convert_ids_to_tokens(input_ids)

# from striki
# input_ids= input_ids[:384]
# tokens = tokens[:384]
input_ids= input_ids[:512]
tokens = tokens[:512]

# For each token and its id...
# for _token, _id in zip(tokens, input_ids):

#     # If this is the [SEP] token, add some space around it to make it stand out.
#     if _id == tokenizer.sep_token_id:
#         print('')

#     # Print the token string and its ID in two columns.
#     print('{:<12} {:>6,}'.format(_token, _id))

#     if _id == tokenizer.sep_token_id:
#         print('')

# Search the input_ids for the first instance of the `[SEP]` token.
sep_index = input_ids.index(tokenizer.sep_token_id)

# The number of segment A tokens includes the [SEP] token istelf.
num_seg_a = sep_index + 1

# The remainder are segment B.
num_seg_b = len(input_ids) - num_seg_a

# Construct the list of 0s and 1s.
segment_ids = [0]*num_seg_a + [1]*num_seg_b

# There should be a segment_id for every input token.
assert len(segment_ids) == len(input_ids)

# Run our example through the model.
start_scores, end_scores = model(torch.tensor([input_ids]),  # The tokens representing our input text.
                                 token_type_ids=torch.tensor([segment_ids]))  # The segment IDs to differentiate question from answer_text

# Find the tokens with the highest `start` and `end` scores.
answer_start = torch.argmax(start_scores)
answer_end = torch.argmax(end_scores)

# Combine the tokens in the answer and print it out.
answer = ' '.join(tokens[answer_start:answer_end+1])
print('Answer: "' + answer + '"')
