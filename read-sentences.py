domain_content = open("domain-content.txt", "r", encoding="UTF-8", errors='ignore')
txt = domain_content.read()
domain_content.close()

sentences = txt.split(". ")

f = open("sentences.txt", "w", encoding="UTF-8", errors="ignore")
for sentence in sentences:
    last_char = sentence[-1:]
    if not(last_char in "?!:"):
        sentence += "."
    f.write(sentence + "\n")
f.close()

print("sentences#: " + str(len(sentences)))
