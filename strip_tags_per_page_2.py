"""
Writes one text file per paragraph containing page title, description and paragraph.
"""

from bs4 import BeautifulSoup
from strip_tags_common import collect_html_files, fix_text, write_paragraph, TXT_FOLDER
import shutil
from os import path
import os

if path.exists(TXT_FOLDER):
    shutil.rmtree(TXT_FOLDER)
os.mkdir(TXT_FOLDER)

for html_file_name in collect_html_files():
    with open(html_file_name, "r", encoding="UTF-8", errors='ignore') as f:
        html_text = f.readlines(). __str__()

    soup = BeautifulSoup(html_text, features = 'lxml')
    # title = soup.find('title')
    title = soup.find("meta",  property="og:title")
    title = title["content"] if title else ""
    title = fix_text(title)

    description = soup.find("meta", property="og:description")
    description = description["content"] if description else ""
    description = fix_text(description)

    paragraphs = soup.find_all('p')

    for paragraph in paragraphs:
        paragraph_text = ""
        paragraph_text += title + ". " if title != "" else ""
        paragraph_text += description + ". " if description != "" else ""
        paragraph_text += fix_text(paragraph.text)
        write_paragraph(html_file_name=html_file_name, paragraph_text=paragraph_text)
