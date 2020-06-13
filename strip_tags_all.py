from bs4 import BeautifulSoup
import os


def fix_text(txt):
    while txt.find('  ') != -1:
        txt = txt.replace('  ', ' ')
    txt = txt.replace('\\n', '')

    if txt.find(" ', '  ', ") != -1:
        txt = txt[0:len(txt) - 10]
    while txt.startswith(" ', ' "):
        txt = txt[6:len(txt)-1]

    txt = txt.replace('\', \' -', ' ')
    txt = txt.replace('\', \'', ' ')
    txt = txt.replace('  ', ' ').replace('  ', ' ').replace('  ', ' ')
    txt = txt.replace('&nbsp;', ' ')
    txt = txt.replace(' \', "  ', ' ')
    txt = txt.replace('", \'', ' ')
    txt = txt.replace(', ', ' ')
    txt = txt.replace('\'" ', ' ')
    txt = txt.replace('"', ' ')
    # txt = txt.replace('-', '. ')
    txt = txt.replace("[' '  ", " ")
    txt = txt.replace("3. D", "3-D")
    txt = txt.replace("i.e.", "ie")
    txt = txt.replace("e.g.", "eg")
    txt = txt.replace("\\'","\'")
    txt = txt.replace("\\t", "")
    txt = txt.replace("\\u200b", "")

    if txt[0:1] == ' ':
        txt = txt[1:]

    if txt[-1:] == ' ':
        txt = txt[0:-1]

    if txt[0:2] == '- ':
        txt = txt[2:]

    txt = txt.replace("\t", "")
    txt = txt.replace("title= Popover on bottom >", "")
    txt = txt.replace(" > Display Address", "")
    txt = txt.replace(" '", "")

    # txt = txt.strip()

    return txt


current_dir = os. path.abspath(os. getcwd())

pars = []

html_files = []
for root, _, files in os.walk(current_dir + '/html/'):
    for file in files:
        if '.html' not in file:
            continue
        p=os. path.join(root,file)
        html_files.append(p)

for h in html_files:
    try:
        html_file = open(h, "r", encoding="UTF-8", errors='ignore')
        txt = html_file.readlines(). __str__()
        html_file.close()
    except:
        pass

    soup = BeautifulSoup(txt, features = 'html.parser')

    for script in soup([
            'script',
            'style',
            'img',
            'iframe'
            ]):
        script.decompose()

    prev_strip = ""

    for strip in soup.stripped_strings:
        strip = fix_text(strip)
        if len(strip) <= 2:
            continue

        if prev_strip[-1:] == ",":
            prev_strip += " " + strip
            continue

        if prev_strip[-1:] == "'":
            prev_strip += " " + strip
            continue

        if len(prev_strip) >= 3:
            if prev_strip.lower()[-3:] == " of":
                prev_strip += " " + strip
                continue

        if len(prev_strip) >= 4:
            if prev_strip.lower()[-4:] == " and":
                prev_strip += " " + strip
                continue

        if len(prev_strip) >= 4:
            if prev_strip.lower()[-4:] == " the":
                prev_strip += " " + strip
                continue

        if not strip[0].isupper():
            prev_strip += " " + strip
            continue

        if strip[0].isupper():
            prev_strip = prev_strip.replace("P.O.", "PO")
            prev_strip = prev_strip.replace("\t", "")
            prev_strip = prev_strip.replace("  ", " ").replace("  ", " ")
            prev_strip = prev_strip.replace(" ' ", ". ")
            if len(prev_strip)>0 and prev_strip[-1:] != ".":
                prev_strip += "."
            if len(prev_strip)>0 and prev_strip not in pars:
                pars.append(prev_strip)

        prev_strip = strip


content = '. '.join(pars)
content = content.replace("..", ".")
content = content.replace("Dr.", "Dr")
# content = content.replace(".", "..")
content = content.replace("1..0", "1.0")
content = content.replace("2..0", "2.0")
content = content.replace("3..0", "3.0")
content = content.replace(":..", ": ")
content = content.replace("  ", " ").replace("  ", " ")
content = content.replace(" ..", "..")
content = content.replace(" ’s", "’s")

with open("domain-content.txt", "w", encoding="UTF-8" , errors='ignore') as content_file:
    content_file.write(content)
