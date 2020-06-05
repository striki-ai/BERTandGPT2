from bs4 import BeautifulSoup
import os
# from langdetect import detect
from langid.langid import LanguageIdentifier, model
identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)

current_dir = os.path.abspath(os.getcwd())

html_files = []
for root, _, files in os.walk(current_dir + '../html/'):
    for file in files:
        if '.html' not in file:
            continue
        p=os.path.join(root,file)
        html_files.append(p)

for h in html_files:
    try:
        html_file = open(h,"r")
        txt = html_file.readlines().__str__()
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
    
    strips =[]

    for strip in soup.stripped_strings:
        while strip.find('  ') != -1:
            strip = strip.replace('  ', ' ')
        strip = strip.replace('\\n', '')
    
        if strip.find(" ', '  ', ") != -1:
            strip = strip[0:len(strip) - 10]
        while strip.startswith(" ', ' "):
            strip = strip[6 : len(strip) - 1]

        if len(strip) >= 32:
            strips.append(strip)

    txt='\n'.join(strips)
    txt = txt.replace('\', \' -', ' ')
    txt = txt.replace('\', \'', ' ')
    txt = txt.replace('  ', ' ').replace('  ', ' ').replace('  ', ' ')
    txt = txt.replace('&nbsp;', '')

    try:
        lang = identifier.classify(txt)[0]
        # lang = detect(txt)
        if lang != 'en':
            continue
    except:
        continue

    h = h.replace(".html", ".txt")
    txt_file = open(h,"w")
    txt_file.write(txt)
    txt_file.close()
