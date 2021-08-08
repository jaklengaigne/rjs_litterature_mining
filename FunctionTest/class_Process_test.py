import pandas as pd
import matplotlib.pyplot as plt
import math
import geonamescache
import folium
from folium.plugins import MarkerCluster

class Process:
    # Method
    """
    Creating a dataframe [3x1]. The first row contain the number of abstract
    (article) mentioning 1 word. The second is the number for another word. The
    third and last one is the number of article that mentioned both.
    Input :     word1        word to count how many article mention it (String)
                word2        word to count how many article mention it (String)
                df          dataframe that contain the column (see below)
                col_words   column's name of the dataframe where to search both words (String)
    Return :    nb_word_by_year
    Save :      plot bar (x,y) → (Publication Year, number of article)
    """
    def nb_art_vs_2sub(self, word1, word2, df, col_words):
        # Defining the words to look for
        word1_list = [word1]
        word2_list = [word2]
        # Adding columns 'Micro' and 'Nano'. Putting True in according cell if word is found.
        df['Word1'] = df[col_words].apply(lambda x: any([k in x for k in word1_list]))
        df['Word2'] = df[col_words].apply(lambda x: any([k in x for k in word2_list]))
        # Adding column to check if an article write about both, if so put True in the cell
        df['Both'] = (df['Word1'] == True) & (df['Word2'] == True)
        # Counting the number of true for each new columns
        # one method
        word1_art = df.value_counts('Word1').loc[True]
        # other method
        word2_art = df['Word2'].sum()
        both_art = df['Both'].sum()
        # Creating a dataframe with those information
        nb_art_2sub = {'Occurence': [word1_art, word2_art, both_art]}
        nb_art_2sub_df = pd.DataFrame(nb_art_2sub, index=[word1, word2, 'both'])
        # Deleting all the new columns because this particular analyse is done
        del df['Word1']
        del df['Word2']
        del df['Both']
        return nb_art_2sub_df
    

    """
    Creating a dataframe [nrow X 2]. The first colunms contain the title of abstract
    (article) mentioning the word. The second is the unique number of the article.
    Input :     word        word used to filter and keep article mentionning it (String)
                df          dataframe that contain the column (see below)
                col_word    column's name of the dataframe where to search the word (String)
                col_info    column's name of the dataframe where the title is (String)
                col_ID      column's name of the dataframe where the unique number is (String)
    Return :    art_with_word   dataframe [nrow X 2]
    """
    def article_with_word(self, word, df, col_word, col_info, col_ID):
        # Defining the words to look for
        word_list = [word]
        # Adding columns 'word'. Putting True in according cell if word is found.
        df[word] = df[col_word].apply(lambda x: any([k in x for k in word_list]))
        # Keeping only the rows containing True (the word is in it)
        art_with_word = df[df[word] == True]
        # Refining the dataframe to be easily use as a check list
        art_with_word = pd.concat([art_with_word[col_info], art_with_word[col_ID]], axis=1)
        # Removing the added columns because it is no more useful
        del df[word]
        return art_with_word
    
    
    """
    Defining a function that create an histogram of number of articles mentioning a
    certain clean word by publication year.
    Note : this function replace NaN made into 'NaN' to 0.
    Input :     word        word that is want to count by year (List of one string element)
                df          dataframe that contain the two columns
                col_word    column's name of the dataframe where to search the word (String)
                col_year    column's name of the dataframe where it is store the year of publication (String)
                plot_title  Title of the plot (String)
                path        Where to save the plot (String)
    Return :    nb_word_by_year
    Save :      plot bar (x,y) → (Publication Year, number of article)
    """
    def plot_word_by_year(self, word, df, col_word, col_year, path):
        # Adding a new columns in df and if word in it put True un cell, else False
        df['Word'] = df[col_word].apply(lambda x: any([k in x for k in word]))
        # Creating a new datafram with the pub year columns and removing 'NaN' → all int
        col_year_noStr = pd.DataFrame(df[col_year].replace('NaN', 0))
        # Getting the publication year without duplicates as an index
        nb_art_by_year = col_year_noStr.value_counts().sort_index()
        nb_art_by_year = pd.DataFrame(nb_art_by_year)
        # Creating a list from the index that have the years without duplicates
        pub_year = pd.DataFrame(nb_art_by_year).index.sort_values().tolist()
        # Creating a dataframe with two columns (year, count), count inisialize at 0
        nb_word_by_year = pd.DataFrame(pub_year, columns=['Publication Year'])
        nb_word_by_year['Count'] = 0
        # Initializing the loop and counting nb of instance of the word by year
        i = -1
        for article in df[col_year]:
            i += 1
            j = -1
            for year in nb_word_by_year['Publication Year']:
                j += 1
                if (df.at[i, 'Word'] == True) & (col_year_noStr.at[i, col_year] == year):
                    nb_word_by_year.at[j, 'Count'] += 1
        # Removing the columns with the true or false indicating if the word is in it
        del df['Word']
        # Converting the year (int) into str in the dataframe used to plot → no bar
        # in year with no pub : so 0-2000 is not a problem
        nb_word_by_year['Publication Year'] = nb_word_by_year['Publication Year'].astype(int).astype(str)
        # Plotting the dataframe and saving it in a folder
        fig = plt.figure()
        axes = fig.add_subplot()
        axes.bar(nb_word_by_year['Publication Year'], nb_word_by_year['Count'], color='orchid')
        axes.set_xlabel('Publication Year')
        axes.set_ylabel('Number of article with ' + word[0])
        axes.set_title('Number of article mentionning ' + word[0] + ' by year')
        plt.xticks(rotation=65)
        min_y = min(nb_word_by_year['Count'])
        max_y = max(nb_word_by_year['Count'])
        y_increment_by_1 = range(math.floor(min_y), math.ceil(max_y)+1)
        plt.yticks(y_increment_by_1)
        plt.gcf().subplots_adjust(bottom=0.20)
        plt.savefig(path)
        # Return the dataframe
        return nb_word_by_year
    
    
    # =============================================================================
    # Based on :
    # Oh, J. (2020, April 23). Using Python to create a world map from a list of country names.
    # Medium. https://towardsdatascience.com/using-python-to-create-a-world-map-from-a-list-of-country-names-cd7480d03b10
    # =============================================================================
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
    def map_publisher_city(self, df, col_city, path):
        # Get a dictionnary of cities
        gc = geonamescache.GeonamesCache()
        cities_dic = gc.get_cities()
        # Transform dictionary into dataframe
        allCity_df = pd.DataFrame(cities_dic).transpose()
        # Change the modified dataframe index because it is not sorted so it make key error otherwise
        allCity_df = allCity_df.reset_index()
        # Refine the dataframe to be less heavy (useless info for us)
        allCity_dfm = allCity_df.drop(['index', 'countrycode', 'population', 'timezone', 'admin1code'], axis=1)
        # Put every letters in capitals because it is like that in my database
        allCity_dfm['name'] = allCity_dfm['name'].str.upper()
        # Replace word : letter with specials caracters for the same letter without it
        clean_name = []
        for name in allCity_dfm['name']:
            clean_name.append(name.replace("À", "A").replace("Â", "A").replace("Á", "A").replace("Ä", "A").replace("Ã", "A").replace("Ā", "A").replace("Ą", "A").replace("È", "E").replace("Ê", "E").replace("É", "E").replace("Ë", "E").replace("Ẽ", "E").replace("Ę", "E").replace("Ì", "I").replace("Î", "I").replace("Í", "I").replace("Ï", "I").replace("Ĩ", "I").replace("Ī", "I").replace("Ò", "O").replace("Ô", "O").replace("Ó", "O").replace("Ö", "O").replace("Õ", "O").replace("Ō", "O").replace("Ù", "U").replace("Û", "U").replace("Ú", "U").replace("Ü", "U").replace("Ũ", "U").replace("Ū", "U").replace("Ç", "C").replace("Ḏ", "D").replace("Ń", "N").replace("Ñ", "N").replace("Ś", "S").replace("Ş", "S").replace("Ź", "Z").replace("Ż", "Z").replace("Ţ", "T").replace("Ł", "T").replace("–", "-").replace("-", " ").replace("’", " ").replace("‘", " ").replace("'", " ").replace("̧ ", " ").replace(".", "").replace("  ", " "))
        allCity_dfm['name'] = clean_name
        # Exploring the database and add latitude and longitude of the publisher's city
        df['Latitude'] = 0.0
        df['Longitude'] = 0.0
        for i in range(len(df)):
            for j in range(len(allCity_dfm)):
                if (df.at[i, col_city] == allCity_dfm.at[j, 'name']):
                    df.at[i, 'Latitude'] = allCity_dfm.at[j, 'latitude']
                    df.at[i, 'Longitude'] = allCity_dfm.at[j, 'longitude']
        # Drop rows with no correspondence in a new dataframe
        map_df = pd.DataFrame(columns=[col_city, 'Latitude', 'Longitude'])
        map_df[col_city] = df[col_city]
        map_df['Latitude'] = df['Latitude']
        map_df['Longitude'] = df['Longitude']
        map_dfm = map_df[(map_df[['Latitude', 'Longitude']] != 0).all(axis=1)]
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
            folium.CircleMarker(location=[lat, lon], radius=rad, popup=popup_text, fill=True).add_to(marker_cluster)
        # Save the fill world map
        world_map.save(path)
        return df

a = ['TROIS RIVIERES', 'Choco', 'Choco-fraise', 'choco', 'Choco', 'glace', 'fraise', 'Limonade', 'sucrée']
b = [1, 1997, 1997, 2, 7, 3, 2021, -1, 0]
c = ['titre1', 'titre2', 'titre3', 'titre4', 'titre5', 'titre6', 'titre7', 'titre8', 'titre9']
df = pd.DataFrame()
df['A'], df['B'], df['C'] = a, b, c

test1 = Process().nb_art_vs_2sub('Choco', 'fraise', df, 'A')
test2 = Process().article_with_word('Choco', df, 'A', 'C', 'B')
test3 = Process().plot_word_by_year(['Choco'], df, 'A', 'B', './TestPlot/TestClass_wordByYear.svg')
test4 = Process().map_publisher_city(df, 'A', './TestPlot/TestClass_map.html')