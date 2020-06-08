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

    if txt[0:1] == ' ':
        txt = txt[1:]

    if txt[-1:] == ' ':
        txt = txt[0:-1]

    if txt[0:2] == '- ':
        txt = txt[2:]

    txt = txt.replace("\t", "")

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
        pass
    except:
        continue

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

        if len(prev_strip) >= 3:
            if prev_strip.lower()[-3:] == " of":
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
            prev_strip = prev_strip.replace("\t", "")
            if prev_strip not in pars:
                pars.append(prev_strip)
        
        prev_strip = strip


content = '. '.join(pars)

with open("domain-content.txt", "w", encoding="UTF-8" , errors='ignore') as content_file:
    content_file.write(content)
