import os


def fix_text(text:str):
    text = text.replace("\\n', '", " ")
    text = text.replace("\\'", " ")
    text = text.replace("['  \\n', \"\\n\", '", " ")
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

