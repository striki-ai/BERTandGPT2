"""[summary]
Common functions used for text extraction from html pages.
"""


import os
import re


paragraph_count =  1
current_dir = os.path.dirname(os.path.realpath(__file__))
TXT_FOLDER = "txt1"
HTML_FOLDER = "html1"


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


def write_paragraph(html_file_name: str, paragraph_text: str):
    """Writes paragraph on disk for search. Adds web address of the page containing the text and extracted from html_file_name.

    Args:
        html_file_name (str): html file name that contains extracted paragraph text. Used for composing web page url that contains extracted paragraph text.
        paragraph_text (str): Text extracted from file with html_file_name file name.
    """
    global paragraph_count

    if paragraph_text == "":
        return

    html_url = html_file_name.replace(current_dir + "/" + HTML_FOLDER + "/", "").replace("\\", "/")
    html_url_in_file_name = html_url \
        .replace("/", "___")

    while paragraph_text.find("\n\n") != -1:
        paragraph_text = paragraph_text.replace("\n\n", "\n")
    # paragraph_text = html_url + "\n\n" + paragraph_text
    # paragraph_text = paragraph_text + "\n\n" + html_url

    paragraph_file_name = current_dir + "/" + TXT_FOLDER + "/" + html_url_in_file_name + "." + "{:0>5d}".format(paragraph_count) + ".txt"

    with open(paragraph_file_name, "w", encoding="UTF-8", errors="ignore") as f:
        f.write(paragraph_text)

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
