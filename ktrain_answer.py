from ktrain import text
from ktrain_config import DATASET_NAME
import sys

question = sys.argv[1]

qa = text.SimpleQA(DATASET_NAME + "/index")
answers = qa.ask(question=question)

# qa.display_answers(answers[:5])

df = qa.answers2df(answers)

# print(df)
print("=" * 80)
print(question)
print("-" * 80)

for i in range(len(df)):
    row = df.iloc[i]
    print("=" * 80)
    print(row["Candidate Answer"])
    print("-" * 80)
    print(row["Context"])