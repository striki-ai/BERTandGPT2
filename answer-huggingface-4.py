from transformers import pipeline
import os
import datetime
import torch

question = "what is machine learning?"

print("Question: " + question)

start_at = datetime.datetime.now()

current_dir = os.path.abspath(os.getcwd())

txt_files = []
for root, _, files in os.walk(current_dir + '/html/'):
    for file in files:
        if '.txt' not in file:
            continue
        p=os.path.join(root,file)
        txt_files.append(p)

nlp = pipeline("question-answering")

answers = []

max_tokens = 100
pre_tokens = 20

max_files_count = 50
files_count = 0

for t in txt_files:

    print(".", end="")
    
    try:
        txt_file = open(t,"r")
        answer_text = txt_file.read()
        txt_file.close()
        pass
    except:
        continue

    files_count += 1

    if files_count > max_files_count:
        break

    total_input = answer_text.split()

    while len(total_input) >= max_tokens:
        
        input = total_input[:max_tokens]
        total_input = total_input[max_tokens-pre_tokens:]

        # response = nlp(question=question, context=input)
        if __name__ == '__main__':
            torch.multiprocessing.freeze_support()
            
        print(nlp(question=question, context=input))

        # if response.answer == "" or response.answer in answers: 
        #     continue

        # answer = answer.lower()
        # answer = answer.replace(" ##", "")
        # answers.append(response.answer)

        # print("\nScore: " + str(response.score))
        # print('\nAnswer: ' + response.answer)
        # print('Text with answer: ' + input)

stop_at = datetime.datetime.now()

print("\nExecuted in " + str((stop_at - start_at)))
