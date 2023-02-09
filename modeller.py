import os
import numpy as np
import lda 
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import csv
import pandas as pd
import gensim
from gensim.utils import simple_preprocess

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

hymns = pd.read_csv('hymns.csv')
oldhymns = pd.read_csv('oldhymns.csv')

hymns['Content'] = \
  hymns['Content'].map(lambda x: re.sub('[,\.!?]', '', x))
