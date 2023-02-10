import os
import nltk
import csv
import pandas as pd

import spacey
from spacy import displacy
NER = spacy.load("en_core_web_sm")

filelocation = input("Input file location: ")
name = input("Desired file name with .csv: ")
files= [k for k in next(os.walk(f"{filelocation}"))][2]
filenames = []
content=[]
for file in files:
    with open(f"{filelocation}\\{file}", 'r', newline='') as source_file:
        filenames.append(file)
        lines = source_file.read()
        content.append(lines)

data = {'Filename':filenames,
        'Content':content}

df = pd.DataFrame(data)
df.to_csv(name, index=False)

# Coming back later

newhymns = pd.read_csv('new_hymns.csv')
oldhymns = pd.read_csv('oldhymns.csv')

oldhymns['Content'] = oldhymns['Content'].str.replace('[^\w\s]', '')
oldhymns['Content'] = oldhymns['Content'].str.replace('\d+', '')

newhymns['Content'] = newhymns['Content'].str.replace('[^\w\s]', '')
newhymns['Content'] = newhymns['Content'].str.replace('\d+', '')

with open('old_hymn_cleaned.txt', 'w', encoding = 'latin-1') as f:
  for text in oldhymns['Content'].tolist():
    f.write(text + '\n')

with open('new_hymn_cleaned.txt', 'w') as f:
  for text in newhymns['Content'].tolist():
    f.write(str(text) + '\n')

#Even later

with open('new_hymn_cleaned.txt', 'r') as file:
    newhymns = file.read()

with open('old_hymn_cleaned.txt', 'r') as file:
    oldhymns = file.read()

new1 = NER(newhymns)
old1 = NER(oldhymns)

displacy.serve(old1, style="ent")
displacy.serve(new1, style="ent")

# http://localhost:5000/
