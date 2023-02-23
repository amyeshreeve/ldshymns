import os
import nltk
import csv
import pandas as pd
from itertools import *

import spacy
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

newhymns['Content'] = newhymns['Content'].str.replace('\r', '')
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

oldentities = {key: list(g) for key, g in groupby(sorted(old1.ents, key=lambda x: x.label_), lambda x: x.label_)}
newentities = {key: list(g) for key, g in groupby(sorted(new1.ents, key=lambda x: x.label_), lambda x: x.label_)}

print(oldentities['LOC'])

# iterate over for unique tokens
# compare

oldpeople = oldentities['PERSON']
oldpeople = map(str, oldpeople)
oldpeople = list(oldpeople)
olddict = {}

for i in oldpeople:
    if i in olddict: olddict[i] += 1
    else: olddict[i] = 1

dict(sorted(olddict.items(), key=lambda item: item[1]))

# make token entities into df

oldents = []
old_attributes = [[ent.text,ent.label_] for ent in old1.ents]
old_df = pd.DataFrame(old_attributes, columns=(["word", "label"]))
old_df.to_excel("old_entities.xlsx")

newents = []
new_attributes = [[ent.text,ent.label_] for ent in new1.ents]
new_df = pd.DataFrame(new_attributes, columns=(["word", "label"]))
new_df.to_excel("new_entities.xlsx")

#reimport cleaned data
#geocode
#map
