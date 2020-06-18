from ktrain import text
import os
from os import path
import shutil

INDEX_DIR = "tmp/index"
TXT_DIR = "wiki_txt"

if path.exists(INDEX_DIR):
    shutil.rmtree(INDEX_DIR)

text.SimpleQA.initialize_index(INDEX_DIR)
file_count = sum((len(f) for _, _, f in os.walk(TXT_DIR)))
text.SimpleQA.index_from_folder(TXT_DIR, INDEX_DIR, commit_every=file_count)

# qa = text.SimpleQA(INDEX_DIR)
# answers = qa.ask("dummy question")
