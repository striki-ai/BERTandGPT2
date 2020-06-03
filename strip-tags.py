from bs4 import BeautifulSoup

html_file = open("C:\\Striki\\BERT\\html\\20080130-sbb-nets.html","r")
txt = html_file.readlines().__str__()
html_file.close()

soup = BeautifulSoup(txt, features = 'html.parser')

for script in soup([
    'script',
    'style',
    'img'
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

txt_file = open("C:\\Striki\\BERT\\html\\20080130-sbb-nets.txt","w")
txt_file.write(txt)
txt_file.close()

print(txt)