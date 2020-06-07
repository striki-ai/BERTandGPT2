from bs4 import BeautifulSoup
import os
from langid. langid import LanguageIdentifier, model

MIN_STRIP_CHARS = 16

domain_content_paras = []

lang_identifier = LanguageIdentifier. from_modelstring(model, norm_probs=True)

current_dir = os. path. abspath(os. getcwd())

# generate list of all html files to be parsed
html_files = []
for root, _, files in os. walk(current_dir + '\\html\\'):
    for file in files:
        if '. html' not in file:
            continue
        p=os. path. join(root,file)
        html_files. append(p)

# Go through all of html files and extract text from them. 
# Add that text as set of paragraphs to domain_content file. 
for h in html_files:
    try:
        html_file = open(h,"r")
        txt = html_file. readlines(). __str__()
        html_file. close()
        pass
    except:
        continue

    soup = BeautifulSoup(txt, features = 'html. parser')

    for script in soup([
            'script',
            'style',
            'img',
            'iframe'
            ]):
        script. decompose()
    
    strips =[]

    for strip in soup. stripped_strings:
        while strip. find('  ') != -1:
            strip = strip. replace('  ', ' ')
        strip = strip. replace('\\n', '')
    
        if strip. find(" ', '  ', ") != -1:
            strip = strip[0:len(strip) - 10]
        while strip. startswith(" ', ' "):
            strip = strip[6 : len(strip) - 1]

        strip = strip. replace('\', \' -', ' ')
        strip = strip. replace('\', \'', ' ')
        strip = txt. replace('  ', ' '). replace('  ', ' '). replace('  ', ' ')
        strip = txt. replace('&nbsp;', '')

        if len(strip) < MIN_STRIP_CHARS:
            continue

        strips. append(strip)

    try:
        lang = lang_identifier. classify(' '. join(strips))[0]
        if lang != 'en':
            continue
    except:
        continue

    domain_content_paras. extend(strips)

with open("domain-content. txt", "w") as domain_content:
    domain_content. write("\n\n". join(domain_content_paras))
