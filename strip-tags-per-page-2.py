from bs4 import BeautifulSoup
import os


def fix_text(text:str):
    text = text.replace("\\n', '", " ")
    text = text.replace("\\'", "")
    text = text.replace("['  \\n', \"\\n\", '", "")
    text = text.replace("&nbsp;", " ")
    while "  " in text:
        text = text.replace("  ", " ")
    text = text.strip()
    return text


paragraph_count =  1
paragraphs_list = []
current_dir = os. path.abspath(os. getcwd())


def write_paragraph(txt:str):
    global paragraphs_list
    global paragraph_count

    if txt == "":
        return

    if (txt in paragraphs_list):
        return

    paragraphs_list.append(txt)

    paragraph_file_name = current_dir + "/txt/" + "{:0>5d}".format(paragraph_count) + ".txt"

    with open(paragraph_file_name, "w", encoding="UTF-8", errors="ignore") as f:
        f.write(txt)

    paragraph_count += 1


pars = []

html_files = []
for root, _, files in os.walk(current_dir + '/html/'):
    for file in files:
        if '.html' not in file:
            continue
        p=os. path.join(root,file)
        html_files.append(p)

for h in html_files:
    with open(h, "r", encoding="UTF-8", errors='ignore') as f:
        html_text = f.readlines(). __str__()

    soup = BeautifulSoup(html_text, features = 'lxml')
    # title = soup.find('title')
    title = soup.find("meta",  property="og:title")
    title = fix_text(title["content"]) if title else ""

    description = soup.find("meta", property="og:description")
    description = fix_text(description["content"]) if description else ""

    paragraphs = soup.find_all('p')

    txt_file_name = h.replace("/html/", "/txt/").replace(".html", ".txt")

    for paragraph in paragraphs:
        paragraph_text = ""
        paragraph_text += title + ". " if title != "" else ""
        paragraph_text += description + ". " if description != "" else ""
        paragraph_text = fix_text(paragraph.text)
        write_paragraph(paragraph_text)
