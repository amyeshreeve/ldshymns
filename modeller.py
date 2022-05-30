import os
import numpy as np
import lda 
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

folder = input("Input folder with .txt files: ")
outputname = input("Input the name of the output file with .txt: ")

os.chdir(folder)
names = os.listdir()

def read_files_into_string(filenames):
  strings= []
  for filename in filenames:
    with open(f'{filename}', encoding ='latin-1') as f:
      text_tokens = word_tokenize(f.read())
      tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
      listToStr = ' '.join([str(elem) for elem in tokens_without_sw])
      strings.append(listToStr)
      print(filename + " added to strings")
  return '\n'.join(strings)

text = read_files_into_string(names)
text = str(text)
document_split = text.split('\n\n\n\n\n')

from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(document_split)
vocabulary = vectorizer.get_feature_names()
import lda
model = lda.LDA(n_topics = 10, n_iter=1000, random_state=1)
model.fit(X)

topic_word = model.topic_word_
n_top_words=50

os.chdir("..")
outfile = open(outputname, "w", encoding="latin-1")

for i, topic_distribution in enumerate(topic_word):
  topic_words = np.array(vocabulary)[np.argsort(topic_distribution)][:-(n_top_words+1):-1]
  print('topic {}: {}'.format(i, ' '.join(topic_words)))
  outfile.write('topic {}: {}'.format(i, ' '.join(topic_words)))
  outfile.write('\n')
  print()

outfile.close()