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
# make token entities into df

oldents = []
old_attributes = [[ent.text,ent.label_] for ent in old1.ents]
old_df = pd.DataFrame(old_attributes, columns=(["word", "label"]))

newents = []
new_attributes = [[ent.text,ent.label_] for ent in new1.ents]
new_df = pd.DataFrame(new_attributes, columns=(["word", "label"]))

#reimport cleaned data

new_locs = new_df.loc[new_df[1].isin(["LOC", "GPE"])]
old_locs = old_df.loc[old_df[1].isin(["LOC", "GPE"])]
old_locs = old_locs.rename(columns={0:'Location', 1:'Tag'})
old_locs = old_locs.drop(columns=["Unnamed: 0"])

new_locs = new_locs.rename(columns={0:'Location', 1:'Tag'})
new_locs = new_locs.drop(columns=["Unnamed: 0"])

#geocode

import geopandas as gpd 
import geopy 
import matplotlib.pyplot as plt
from geopy.extra.rate_limiter import RateLimiter

locator = geopy.geocoders.Nominatim(user_agent=”mygeocoder”)
geocode = RateLimiter(locator.geocode, min_delay_seconds=1)

new_locs['address'] = new_locs['Location'].apply(geocode)
old_locs['address'] = old_locs['Location'].apply(geocode)

new_locs['coordinates'] = new_locs['address'].apply(lambda loc: tuple(loc.point) if loc else None)
new_locs[['latitude', 'longitude', 'altitude']] = pd.DataFrame(new_locs['coordinates'].tolist(), index=new_locs.index)

old_locs['coordinates'] = old_locs['address'].apply(lambda loc: tuple(loc.point) if loc else None)
old_locs[['latitude', 'longitude', 'altitude']] = pd.DataFrame(old_locs['coordinates'].tolist(), index=old_locs.index)

#map

import folium
from folium.plugins import FastMarkerCluster

folium_map = folium.Map(location=[59.338315,18.089960],
  zoom_start=2,
  tiles='CartoDB dark_matter')

FastMarkerCluster(data=list(zip(old_locs['latitude'].values, old_locs['longitude'].values))).add_to(folium_map)
folium.LayerControl().add_to(folium_map)
old_output = "old_hymnbook_map.html"
folium_map.save(old_output)

FastMarkerCluster(data=list(zip(new_locs['latitude'].values, new_locs['longitude'].values))).add_to(folium_map)
folium.LayerControl().add_to(folium_map)
new_output = "new_hymnbook_map.html"
folium_map.save(new_output)
