# -*- coding: utf-8 -*-
"""
Created on Sun May 30 15:21:35 2021

@author: valerie toupin-guay
"""
# ref 
# https://github.com/yaph/geonamescache
# https://towardsdatascience.com/using-python-to-create-a-world-map-from-a-list-of-country-names-cd7480d03b10
# https://www.learnbyexample.org/python-nested-dictionary/



"""
Defining a function that create a map of publisher's city and add latitude and 
longitude in the initial database
Note :  this function DO NOT map cities with no correspondence with the cities
        Can't save in svg, only html works
        Dataframe index migth need to be reset before using this function
dictionary use in this function.
Input :     df          dataframe that contain cities in CAPITALS without specials characters
            col_city    column's name of the dataframe where to search the city (String)
            path        Where to save the map (String that end with .html)
Return :    the dataframe with two new columns (latitude and longitude)
Save :      plot bar (x,y) → (Publication Year, number of article)
"""
def map_publisher_city(df, col_city, path):
    # Libraries
    import geonamescache
    import pandas as pd
    import folium
    from folium.plugins import MarkerCluster   
    # Get a dictionnary of cities
    gc = geonamescache.GeonamesCache()
    cities_dic = gc.get_cities()
    # Transform dictionary into dataframe
    allCity_df =  pd.DataFrame(cities_dic).transpose()
    # Change the modified dataframe index because it is not sorted so it make key error otherwise
    allCity_df = allCity_df.reset_index()
    # Refine the dataframe to be less heavy (useless info for us)
    allCity_dfm = allCity_df.drop(['index', 'countrycode', 'population', 'timezone', 'admin1code'], axis=1)
    # Put every letters in capitals because it is like that in my database
    allCity_dfm['name'] = allCity_dfm['name'].str.upper()
    # Replace word : letter with specials caracters for the same letter without it
    clean_name = []
    for name in allCity_dfm['name']:
        clean_name.append(name.replace("À","A").replace("Â","A").replace("Á", "A").replace("Ä","A").replace("Ã","A").replace("Ā","A").replace("Ą","A").replace("È","E").replace("Ê","E").replace("É","E").replace("Ë","E").replace("Ẽ","E").replace("Ę","E").replace("Ì","I").replace("Î","I").replace("Í","I").replace("Ï","I").replace("Ĩ","I").replace("Ī","I").replace("Ò","O").replace("Ô","O").replace("Ó", "O").replace("Ö","O").replace("Õ","O").replace("Ō","O").replace("Ù","U").replace("Û","U").replace("Ú", "U").replace("Ü","U").replace("Ũ","U").replace("Ū","U").replace("Ç", "C").replace("Ḏ","D").replace("Ń","N").replace("Ñ", "N").replace("Ś","S").replace("Ş","S").replace("Ź","Z").replace("Ż","Z").replace("Ţ","T").replace("Ł","T").replace("–", "-").replace("-", " ").replace("’", " ").replace("‘"," ").replace("'", " ").replace("̧ "," ").replace(".", "").replace("  "," "))
    allCity_dfm['name'] = clean_name
    # Exploring the database and add latitude and longitude of the publisher's city
    df['Latitude'] = 0.0
    df['Longitude'] = 0.0
    for i in range(len(df)):
        for j in range(len(allCity_dfm)):
            if (df.at[i, col_city] == allCity_dfm.at[j, 'name']):
                df.at[i, 'Latitude'] = allCity_dfm.at[j, 'latitude']
                df.at[i,'Longitude'] = allCity_dfm.at[j, 'longitude']
    # Drop rows with no correspondence in a new dataframe
    map_df = pd.DataFrame(columns=[col_city, 'Latitude','Longitude'])
    map_df[col_city] = df[col_city]
    map_df['Latitude'] = df['Latitude']
    map_df['Longitude'] = df['Longitude']
    map_dfm = map_df[(map_df[['Latitude','Longitude']]!=0).all(axis=1)]
    # Create an empty world map
    world_map = folium.Map(tiles="cartodbpositron")
    marker_cluster = MarkerCluster().add_to(world_map)
    # Create circle marker from latitude and longitude (coordinates)
    for i in range(len(map_dfm)):
        lat = map_dfm.iloc[i]['Latitude']
        lon = map_dfm.iloc[i]['Longitude']
        rad = 6
        popup_text = """City : {}<br>"""
        popup_text = popup_text.format(map_dfm.iloc[i][col_city])
        folium.CircleMarker(location=[lat,lon], radius=rad, popup=popup_text, fill=True).add_to(marker_cluster)
    # Save the fill world map
    world_map.save(path)
    return df



import pandas as pd

# test1
dic1 = {0: {'pub_city': 'Québec', 'Num': 1.2},
     1: {'pub_city': 'TROIS RIVIERES', 'Num': 0},
     2: {'pub_city': 'OXFORD', 'Num': 92},
     3: {'pub_city': 'VICTORIAVILLE', 'Num': 890.9},
     4: {'pub_city': 'SEOUL', 'Num': 10},
     5: {'pub_city': 'SEOUL', 'Num': -45}}
df1 = pd.DataFrame(dic1).transpose()
col_city1 = 'pub_city'
path1 = './TestPlot/map_test1.html'
test1 = map_publisher_city(df1, col_city1, path1)