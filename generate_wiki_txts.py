from strip_tags_common import write_paragraph

HTML_FILE_NAME = "wiki"

line = ""
prev_lines = []
cnt = 0

with open("C:/Striki/Temp/wiki.txt", "r", encoding="UTF-8") as f:
    while True:
        line = f.readline()

        if line == "": # EOF detected
            if len(prev_lines) > 0:
                write_paragraph(HTML_FILE_NAME, "\n".join(prev_lines))
            break

        line = line[:len(line)-1].strip() # remove ending /n, leading and ending whitespaces

        if line == "":
            if cnt == 6220:
                print("oo")
            while len(prev_lines) > 0:
                temp_lines = []
                i = 0

                while len(" ".join(temp_lines).split(" ")) - 1 + len(prev_lines[i].split(" ")) <= 384:
                    temp_lines.append(prev_lines[i])
                    i += 1

                    if i >= len(prev_lines) or len(" ".join(temp_lines).split(" ")) >= 384:
                        prev_lines = []
                        i = 0
                        break

                if len(temp_lines) > 0:
                    paragraph_text = "\n".join(temp_lines)
                    if len(paragraph_text.split(" ")) >= 512:
                        print(len(paragraph_text.split(" ")))
                        print("ops")
                    write_paragraph(HTML_FILE_NAME, paragraph_text)
                    cnt += 1
                    prev_lines = prev_lines[len(temp_lines):]
                else:
                    paragraph_text = "\n".join(prev_lines)
                    if len(paragraph_text.split(" ")) >= 512:
                        print(len(paragraph_text.split(" ")))
                        print("ops 222")
                    write_paragraph(HTML_FILE_NAME, paragraph_text)
                    cnt += 1
                    prev_lines = []

            # paragraph_text = "\n".join(prev_lines)
            # if len(paragraph_text.split(" ")) >= 512:
            #     print("ops 2")
            # write_paragraph(HTML_FILE_NAME, paragraph_text)
            # prev_lines = []
        else:
            words = line.split(" ")
            while len(words) > 384:
                prev_lines.append(" ".join(words[:384]))
                words = words[384:]
            prev_lines.append(" ".join(words))
