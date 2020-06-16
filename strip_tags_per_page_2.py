"""
Writes one text file per found title, description and each paragraph.
"""

from bs4 import BeautifulSoup
from strip_tags_common import collect_html_files, fix_text, fix_document, write_paragraph, TXT_FOLDER
import shutil
from os import path
import os

if path.exists(TXT_FOLDER):
    shutil.rmtree(TXT_FOLDER)
os.mkdir(TXT_FOLDER)

for html_file_name in collect_html_files():
    with open(html_file_name, "r", encoding="UTF-8") as f:
        html_text = f.read()
        html_text = fix_document(html_text)

    soup = BeautifulSoup(html_text, features = 'lxml')

    # collect the whole document text as list of texts found in
    # h1, h2 and p html elements
    html_elements = soup.find_all(['h1', 'h2', 'p', 'li'])
    txt_elements = []

    for html_element in html_elements:
        text = fix_text(html_element.text)
        if "Document generated by Confluence on " in text:
            continue
        txt_elements.append(text)

    # compose text with all txt elements joined by " "
    all_texts = " ".join(txt_elements)

    # let now txt_elements be all_text parts splitted by " "
    all_texts = all_texts.split(" ")
    MAX_TOKENS = 384
    PRE_TOKENS = 64

    while len(all_texts) > 0:
        one_doc = all_texts[:MAX_TOKENS]
        all_texts = all_texts[MAX_TOKENS-PRE_TOKENS:]

        one_doc = " ".join(one_doc)
        write_paragraph(html_file_name=html_file_name, paragraph_text=one_doc)
