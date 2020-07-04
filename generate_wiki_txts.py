from strip_tags_common import write_paragraph, MAX_WORDS_IN_PARAGRAPH

line = ""
prev_lines = []
with open("D:/Striki/Temp/wiki.txt", "r", encoding="UTF-8") as f:
    while True:
        line = f.readline()

        if line == "": # EOF detected
            if len(prev_lines) > 0:
                write_paragraph("\n".join(prev_lines))
            break

        line = line[:len(line)-1].strip() # remove ending /n, leading and ending whitespaces

        if line == "":
            while len(prev_lines) > 0:
                temp_lines = []
                i = 0

                while len(" ".join(temp_lines).split(" ")) - 1 + len(prev_lines[i].split(" ")) <= MAX_WORDS_IN_PARAGRAPH:
                    temp_lines.append(prev_lines[i])
                    i += 1

                    if i >= len(prev_lines) or len(" ".join(temp_lines).split(" ")) >= MAX_WORDS_IN_PARAGRAPH:
                        prev_lines = []
                        i = 0
                        break

                if len(temp_lines) > 0:
                    paragraph_text = "\n".join(temp_lines)
                    if len(paragraph_text.split(" ")) > MAX_WORDS_IN_PARAGRAPH:
                        qq = len(paragraph_text.split(" "))
                        print(qq)
                    write_paragraph(paragraph_text)
                    prev_lines = prev_lines[len(temp_lines):]
                else:
                    paragraph_text = "\n".join(prev_lines)
                    if len(paragraph_text.split(" ")) > MAX_WORDS_IN_PARAGRAPH:
                        qq = len(paragraph_text.split(" "))
                        print(qq)
                    write_paragraph(paragraph_text)
                    prev_lines = []
        else:
            words = line.split(" ")
            while len(words) > MAX_WORDS_IN_PARAGRAPH:
                prev_lines.append(" ".join(words[:MAX_WORDS_IN_PARAGRAPH]))
                words = words[MAX_WORDS_IN_PARAGRAPH - 50:]
            prev_lines.append(" ".join(words))
