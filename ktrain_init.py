from ktrain import text
import os
from os import path
import shutil
from ktrain_config import DATASET_NAME

if path.exists(DATASET_NAME + "/index"):
    shutil.rmtree(DATASET_NAME + "/index")

text.SimpleQA.initialize_index(DATASET_NAME + "/index")
file_count = sum((len(f) for _, _, f in os.walk(DATASET_NAME + "/txt")))
text.SimpleQA.index_from_folder(DATASET_NAME + "/txt", DATASET_NAME + "/index", commit_every=file_count, limitmb=4096)

# qa = text.SimpleQA(INDEX_DIR)
# answers = qa.ask("dummy question")
