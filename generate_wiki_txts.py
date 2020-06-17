from strip_tags_common import write_paragraph

HTML_FILE_NAME = "wiki"

line = ""
prev_lines = []

with open("C:/Striki/Temp/wiki.txt", "r", encoding="UTF-8") as f:
    while True:
        line = f.readline()

        if line == "": # EOF detected
            if len(prev_lines) > 0:
                write_paragraph(HTML_FILE_NAME, "\n".join(prev_lines))
            break

        line = line[:len(line)-1].strip() # remove ending /n, leading and ending whitespaces
        if line == "":
            if len(prev_lines) > 0:
                write_paragraph(HTML_FILE_NAME, "\n".join(prev_lines))
                prev_lines = []
        else:
            prev_lines.append(line)