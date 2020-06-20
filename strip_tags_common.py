import os
import re
from ktrain_config import DATASET_NAME

paragraph_count =  1
current_dir = os.path.dirname(os.path.realpath(__file__))

MIN_WORDS_IN_PARAGRAPH = 10


def fix_document(text:str) -> str:
    """Implements firs html input text. For beginning, removes \\n, CDATA and xml comments.

    Args:
        text (str): Input text.

    Returns:
        str: Cleared text.
    """
    text = text.replace(">", ">&nbsp;").replace("\n", " ")
    # remove CDATA from html
    text = re.sub("\[CDATA\[.*?\]\]", " ", text)
    text = re.sub("<!.*?>", " ", text)
    return text

def fix_text(text:str) -> str:
    """Removes parts of input text that are not wanted in text file that will be written for search.

    Args:
        text (str): Input text that is taken from parsed html file.

    Returns:
        [str]: Cleaned text thas sould be written in file for search.
    """

    text = text.replace(u'\xa0', u' ')
    text = text.replace("\\n', '", " ")
    text = text.replace("\\'", " ")
    text = text.replace("['  \\n', \"\\n\", '", " ")
    text = text.replace("&nbsp;", " ")
    while "  " in text:
        text = text.replace("  ", " ")
    text = text.strip()
    return text


def count_words(paragraph_text: str) -> int:
    words_cnt = 0
    lines = paragraph_text.split("\n")
    for line in lines:
        words_cnt += len(line.split(" "))
    return words_cnt

def write_paragraph(paragraph_text: str):
    """Writes paragraph on disk for search. Adds web address of the page containing the text and extracted from html_file_name.

    Args:
        paragraph_text (str): Text extracted from file with html_file_name file name.
    """

    if count_words(paragraph_text) < MIN_WORDS_IN_PARAGRAPH:
        return

    assert len(paragraph_text.split(" ")) < 512

    global paragraph_count

    if paragraph_text == "":
        return

    while paragraph_text.find("\n\n") != -1:
        paragraph_text = paragraph_text.replace("\n\n", "\n")

    # paragraph_text = html_url + "\n\n" + paragraph_text
    # paragraph_text = paragraph_text + "\n\n" + html_url
    # c:/striki/bert/wiki_txt/wiki.123 456 789 012 .txt

    file_name_no_dirs = current_dir + "/" + DATASET_NAME + "/txt/" + "{:0>12d}".format(paragraph_count) + ".txt"
    file_dir = file_name_no_dirs[:-13] + "/" \
        + file_name_no_dirs[-13:-10] + "/" \
        + file_name_no_dirs[-10:-7]
    file_name = file_dir + "/" + file_name_no_dirs[-7:]

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    if not os.path.exists(file_name):
        with open(file_name, "w", encoding="UTF-8") as f:
            f.write(paragraph_text)

    if paragraph_count % 1000 == 0:
        print(paragraph_count)

    paragraph_count += 1


def collect_html_files() -> list:
    """Collects names of all html files found in 'html' subfolder.

    Returns:
        list: List of the names of all html files found in 'html' subfolder.
    """

    html_root_dir = current_dir + "/" + HTML_FOLDER + "/"

    html_files = []
    for root, _, files in os.walk(html_root_dir):
        for file in files:
            if '.html' not in file:
                continue
            p=os. path.join(root,file)
            html_files.append(p)

    return html_files
