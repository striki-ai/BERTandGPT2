domain_content = open("domain-content.txt", "r", encoding="UTF-8", errors='ignore')
txt = domain_content.read()
domain_content.close()

sentences = txt.split(". ")

f = open("sentences.txt", "w", encoding="UTF-8", errors="ignore")
for sentence in sentences:
    f.write(sentence + "\n")
f.close()

print("sentences#: " + str(len(sentences)))
