from bs4 import BeautifulSoup
import os
from langid.langid import LanguageIdentifier, model

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
    txt = txt.replace('-', '. ')

    if txt[0:1] == ' ':
        txt = txt[1:]

    if txt[-1:] == ' ':
        txt = txt[0:-1]

    if txt[0:2] == '- ':
        txt = txt[2:]

    return txt


identifier = LanguageIdentifier. from_modelstring(model, norm_probs=True)

current_dir = os. path. abspath(os. getcwd())

pars = []

html_files = []
for root, _, files in os. walk(current_dir + '/html/'):
    for file in files:
        if '.html' not in file:
            continue
        p=os. path. join(root,file)
        html_files. append(p)

for h in html_files:
    try:
        html_file = open(h,"r")
        txt = html_file. readlines(). __str__()
        html_file. close()
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
        script. decompose()
    
    for strip in soup. stripped_strings:
        strip = fix_text(strip)
        
        if len(strip. split(' ')) > 8:
            if strip not in pars:
                pars. append(strip)

with open("domain-content.txt", "w") as content:
    content. write("\n\n". join(pars))
