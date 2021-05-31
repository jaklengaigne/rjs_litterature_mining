# -*- coding: utf-8 -*-
"""
Created on Sun May 30 15:21:35 2021

@author: valerie toupin-guay
"""
# ref 
# https://github.com/yaph/geonamescache
# https://towardsdatascience.com/using-python-to-create-a-world-map-from-a-list-of-country-names-cd7480d03b10
# https://www.learnbyexample.org/python-nested-dictionary/

import geonamescache
import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster


# Get a dictionnary of cities
gc = geonamescache.GeonamesCache()
cities_dic = gc.get_cities()

# Refined the dictionay to be less heavy (name, longitude and latitude)
''' My code will have flaws because I willl over look alternatenames even though
 they are in the dictionary '''
 # Also, I will put every letters in capitals because it is like that in my database



#a = cities_dic['2758']['name'] # Québec
#b = cities_dic['2729']['name'] # Trois-Rivière
c = cities_dic['10570']['name'] # Alvand : visually first in dic in "Variable Explorer"
#d = cities_dic['13744']['name'] # Busan


test1 = {'id1': {'name': 'Québec', 'lat': 1.2},
     'id2': {'name': 'trois-rivières', 'lat': 0},
     'id3': {'name': 'victoriaville', 'lat': 890.9}}
name1 = []
for key1, info in test1.items():
        name1.append(test1[key1]['name'])



test2 = {900: {'name': 'Québec', 'lat': 1.2},
     0: {'name': 'trois-rivières', 'lat': 0},
     3: {'name': 'Alvand', 'lat': 92},
     12: {'name': 'victoriaville', 'lat': 890.9}}
name2 = []
for key2, info in test2.items():
        name2.append(test2[key2]['name'])
# See that name2 have the same order as in the script
# BUT test2 (nested dictionary) in spyder "Variable Explorer" is in key ascending order



# test3
name3 = []
for key in cities_dic:
    name3.append(cities_dic[key]['name'])



# test 4 other method
name4 = []
for key4, info in cities_dic.items():
    name4.append(cities_dic[key4]['name'])
    
    

# =============================================================================
# # test5 
# name5 = []
# df5 = []
# df5 = pd.DataFrame(df5, columns=['Key', 'Name', 'Longitude', 'Latitude'])
# for key5 in cities_dic:
#     name5.append(cities_dic[key5]['name'])
# df5['Name'] = name5
# =============================================================================



# test6
test6 = {0: {'Publisher City': 'Québec', 'Num': 1.2},
     1: {'Publisher City': 'TROIS RIVIERES', 'Num': 0},
     2: {'Publisher City': 'OXFORD', 'Num': 92},
     3: {'Publisher City': 'VICTORIAVILLE', 'Num': 890.9},
     4: {'Publisher City': 'SEOUL', 'Num': 10},
     5: {'Publisher City': 'SEOUL', 'Num': -45}}
test6_df = pd.DataFrame(test6).transpose()
# Transform dictionary into dataframe
df6 =  pd.DataFrame(cities_dic).transpose()
# Change the modified dataframe index because it is not sorted so it make key error otherwise
df6 = df6.reset_index()
# Refine the dataframe to be less heavy (useless info for us)
df6m = df6.drop(['index', 'countrycode', 'population', 'timezone', 'admin1code'], axis=1)
# Put every letters in capitals because it is like that in my database
df6m['name'] = df6m['name'].str.upper()
# Replace word : letter with specials caracters for the same letter without it
clean_name = []
for name in df6m['name']:
    clean_name.append(name.replace("À","A").replace("Â","A").replace("Á", "A").replace("Ä","A").replace("Ã","A").replace("Ā","A").replace("Ą","A").replace("È","E").replace("Ê","E").replace("É","E").replace("Ë","E").replace("Ẽ","E").replace("Ę","E").replace("Ì","I").replace("Î","I").replace("Í","I").replace("Ï","I").replace("Ĩ","I").replace("Ī","I").replace("Ò","O").replace("Ô","O").replace("Ó", "O").replace("Ö","O").replace("Õ","O").replace("Ō","O").replace("Ù","U").replace("Û","U").replace("Ú", "U").replace("Ü","U").replace("Ũ","U").replace("Ū","U").replace("Ç", "C").replace("Ḏ","D").replace("Ń","N").replace("Ñ", "N").replace("Ś","S").replace("Ş","S").replace("Ź","Z").replace("Ż","Z").replace("Ţ","T").replace("Ł","T").replace("–", "-").replace("-", " ").replace("’", " ").replace("‘"," ").replace("'", " ").replace("̧ "," ").replace(".", "").replace("  "," "))
df6m['name'] = clean_name
# Exploring the database and add latitude and longitude of the publisher's city
# =============================================================================
# test6_df['Latitude'] = test6_df['Publisher City'].apply(lambda x: any([k in x for k in df6m['name']]))
# =============================================================================
test6_df['Latitude'] = 0
test6_df['Longitude'] = 0
for i in range(len(test6_df)):
    for j in range(len(df6m)):
        if (test6_df.at[i, 'Publisher City'] == df6m.at[j, 'name']):
            test6_df.at[i, 'Latitude'] = df6m.at[j, 'latitude']
            test6_df.at[i,'Longitude'] = df6m.at[j, 'longitude']
# =============================================================================
# test6_df['Latitude'] = np.where(test6_df['Publisher City'] == df6m['name'], df6m['latitude'], 'mismatch')
# =============================================================================
# =============================================================================
# test6_df['Latitude'] = test6_df['Publisher City'].apply(lambda x: df6m['latitude'] if x == test6_df['Publisher City'] else 'Mismatch')
# =============================================================================
# Create an empty world map
world_map = folium.Map(tiles="cartodbpositron")
marker_cluster = MarkerCluster().add_to(world_map)
# Create circle marker from latitude and longitude (coordinates)
for i in range(len(test6_df)):
    lat = test6_df.iloc[i]['Latitude']
    lon = test6_df.iloc[i]['Longitude']
    rad = 5
    popup_text = """ """
    popup_text = popup_text.format(test6_df.iloc[i]['Publisher City'])
    folium.CircleMarker(location=[lat,lon], radius=rad, popup=popup_text, fill=True).add_to(marker_cluster)
# Save the fill world map
world_map.save('./TestPlot/map_test6.html')

# =============================================================================
# # dead
# for name in df6m['name']:
#     letter_list = [char for char in name]
#     for letter in letter_list:
#         letter_list[letter].replace("À","A").replace("Â","A").replace("Á", "A").replace("Ä","A").replace("Ã","A").replace("Ā","A").replace("Ą","A").replace("È","E").replace("Ê","E").replace("É","E").replace("Ë","E").replace("Ẽ","E").replace("Ę","E").replace("Ì","I").replace("Î","I").replace("Í","I").replace("Ï","I").replace("Ĩ","I").replace("Ī","I").replace("Ò","O").replace("Ô","O").replace("Ó", "O").replace("Ö","O").replace("Õ","O").replace("Ù","U").replace("Û","U").replace("Ú", "U").replace("Ü","U").replace("Ũ","U").replace("Ū","U").replace("Ç", "C").replace("Ń","N").replace("Ñ", "N").replace("Ś","S").replace("Ź","Z").replace("Ż","Z").replace("Ţ","T").replace("Ł","T").replace("–", "-").replace("-", " ").replace("’", " ").replace("'", " ").replace("̧ "," ").replace(".", "")
#     df6m[name] = letter_list.join()
# =============================================================================

test7 = {900: {'Publisher City': 'Québec', 'Num': 1.2},
     0: {'Publisher City': 'TROIS RIVIERES', 'Num': 0},
     3: {'Publisher City': 'OXFORD', 'Num': 92},
     12: {'Publisher City': 'VICTORIAVILLE', 'Num': 890.9},
     7: {'Publisher City': 'SEOUL', 'Num': 10},
     4: {'Publisher City': 'SEOUL', 'Num': -45}} 
    
# =============================================================================
# df = pd.DataFrame(name)
# df.to_csv('./test_map.csv', sep=';')
# =============================================================================
