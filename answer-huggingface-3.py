import torch
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
import os
import datetime

cuda_device_id = torch. cuda. current_device()
print("cuda device count: " + str(torch. cuda. device_count()))
print("cuda device name: " + torch. cuda. get_device_name(cuda_device_id))
print("cuda is available: " + str(torch. cuda. is_available()))

question = "what is machine learning?"

print("Question: " + question)

start_at = datetime. datetime. now()

current_dir = os. path. abspath(os. getcwd())

txt_files = []
for root, _, files in os. walk(current_dir + '/html/'):
    for file in files:
        if '. txt' not in file:
            continue
        p=os. path. join(root,file)
        txt_files. append(p)

# model_name = 'bert-large-uncased-whole-word-masking-finetuned-squad'
# model = BertForQuestionAnswering. from_pretrained(model_name)
# tokenizer = BertTokenizer. from_pretrained(model_name)

model_name = 'deepset/bert-large-uncased-whole-word-masking-squad2'
model = BertForQuestionAnswering. from_pretrained(model_name)
tokenizer = BertTokenizer. from_pretrained(model_name)

answers = []

max_tokens = 100
pre_tokens = 20

max_files_count = 50
files_count = 0

for t in txt_files:

    print(". ", end="")
    
    try:
        txt_file = open(t,"r")
        answer_text = txt_file. read()
        txt_file. close()
        pass
    except:
        continue

    files_count += 1

    if files_count > max_files_count:
        break

    # answer_text = """BERT-large is really big. . .  it has 24-layers and an embedding
    # size of 1,024, for a total of 340M parameters! Altogether it is 1. 34GB,
    # so expect it to take a couple minutes to download to your Colab instance. """

    # Apply the tokenizer to the input text, treating them as a text-pair. 
    total_input_ids = tokenizer. encode(question, answer_text)

    # BERT only needs the token IDs, but for the purpose of inspecting the
    # tokenizer's behavior, let's also get the token strings and display them. 
    total_tokens = tokenizer. convert_ids_to_tokens(total_input_ids)

    while len(total_input_ids) >= max_tokens:
        
        input_ids = total_input_ids[:max_tokens]
        input_ids. append(tokenizer. sep_token_id)
        tokens = total_tokens[:max_tokens]
        tokens. append("[SEP]")

        total_input_ids = total_input_ids[max_tokens-pre_tokens:]
        # total_tokens = total_tokens[max_tokens-pre_tokens:]

        # Search the input_ids for the first instance of the `[SEP]` token. 
        sep_index = input_ids. index(tokenizer. sep_token_id)

        # The number of segment A tokens includes the [SEP] token istelf. 
        num_seg_a = sep_index + 1

        # The remainder are segment B. 
        num_seg_b = len(input_ids) - num_seg_a

        # Construct the list of 0s and 1s. 
        segment_ids = [0]*num_seg_a + [1]*num_seg_b

        # There should be a segment_id for every input token. 
        assert len(segment_ids) == len(input_ids)

        # Run our example through the model. 
        start_scores, end_scores = model(torch. tensor([input_ids]),  # The tokens representing our input text. 
                                         token_type_ids=torch. tensor([segment_ids]))  # The segment IDs to differentiate question from answer_text

        # Find the tokens with the highest `start` and `end` scores. 
        answer_start = torch. argmax(start_scores)
        answer_end = torch. argmax(end_scores)

        # Combine the tokens in the answer and print it out. 
        answer = ' '. join(tokens[answer_start:answer_end+1])

        if answer == "": 
            continue
        # if answer in answers: 
        #     continue
        if answer. find("[CLS]") != -1 : 
            continue

        # answer = answer. lower()

        answer = answer. replace(" ##", "")
        answers. append(answer)

        text_with_answer = " ". join(tokens)
        text_with_answer = text_with_answer. replace(" ##", ""). replace("##", "")
        text_with_answer = text_with_answer. replace(answer. lower(), ""). replace("[SEP]", "")
                
        print('\nAnswer: ' + answer)
        print('Score: ' + str(torch. max(start_scores)))
        print('Text with answer: ' + text_with_answer)

stop_at = datetime. datetime. now()

print("\nExecuted in " + str((stop_at - start_at)))
