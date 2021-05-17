"""
Base on this tutorial
Chalaguine, L. A. (2020, August 3). Getting started with text analysis in Python. Medium. https://towardsdatascience.com/getting-started-with-text-analysis-in-python-ca13590eb4f7
"""

# Librairies 
import pandas as pd
import re
from nltk.stem import PorterStemmer
from nltk import word_tokenize, bigrams, trigrams
from collections import Counter
import os
import matplotlib.pyplot as plt


# Read the database file
raw_data = pd.read_csv("DataBase_20210503.csv", sep=";")



# Return the data frame of raw_data
raw_data.head



# Removing duplicates if needed
"""
Creating a new column in the data frame. All the colums are considered
because any subset are specified. The fisrt occurence of a row is keep
by writing False in the new column at this row (not a duplicate). Else,
True is writed.
"""
raw_data['dup'] = raw_data.duplicated(subset=None, keep='first')
"""
Counting the number of duplicates (number of true). Return the number
of False and True.
"""
raw_data['dup'].value_counts()
# Creating a new data frame without the duplicates
raw_data_noDup = raw_data[ raw_data['dup']==False ]
"""
Deleting the column with the True and False because because it is
no more useful
"""
del raw_data_noDup['dup']



# Removing useless columns (All articles have written nothing in those fields)
raw_data_useField = raw_data_noDup.dropna(axis=1, how='all')



# Changing the type of NaN to string (For text cleaning everything need to be string)
raw_data_str = raw_data_useField.fillna("NaN")



# Text cleaning (removal of "meaningless" words)
"""
SmartStoplist.txt
by Lisa Andreevna
Lisanka93/text_analysis_python_101. (n.d.). GitHub. Retrieved May 3, 2021, 
from https://github.com/lisanka93/text_analysis_python_101
**** Note : nan is added to Lisa Andreevna's list ****
"""
# Definition of constant and variable
stop_words_file = 'SmartStoplist.txt'
stop_words = []
# Creating a list of stop words while reading the stop words's file
with open(stop_words_file, "r") as f:
    for line in f:
        stop_words.extend(line.split())
# Do not understand yet
stop_words = stop_words
"""
Definition of a cleaning function (preprocess before words analysis)
This function get a text and return a text (string) of stemmed word in 
lowercase without stop words and any caracter except letter
"""
def preprocess(raw_text):
    """
    Keep only letters in the text (lowercase and capitals) using Regex (re). 
    Replace all symboles with a blank space.
    """
    letters_only_text = re.sub("[^a-zA-Z]", " ", raw_text)
    # Change the capitals for lowercase AND split into a list of words (no expression)   
    words = letters_only_text.lower().split()
    # Define a variable to receive only the useful crop (or not) words
    cleaned_words = []
    # Remove stop words (Take word in list of words and make a list of clean words)
    for word in words:
        if word not in stop_words:
            cleaned_words.append(word)
    # Stem word (Creating a new list of stemmed word with the clean one)
    stemmed_words = []
    for word in cleaned_words:
        word = PorterStemmer().stem(word)
        stemmed_words.append(word)
    # After all those changes, convert back the final list into string
    return " ".join(stemmed_words)
# Clean abstracts of all the articles of the research (overwrite)
raw_data_str['Abstract'] = raw_data_str['Abstract'].apply(preprocess)
clean_data = raw_data_str



# Citation's data - extension pack
# Importing
raw_cita_data = pd.read_csv("CitationsData_20210507.csv", sep=";")
# Creating a DataFrame
raw_cita_data.head
# Removing all columns that only contain 0
clean_cita_data = raw_cita_data.loc[:, (raw_cita_data != 0).any(axis=0)]
# Adding this extension to the clean database
clean_data = pd.concat([clean_data, clean_cita_data], axis=1)



# Data exploration
# Most common words in all the abstracts (top 100)
top_hundred = Counter(" ".join(clean_data['Abstract']).split()).most_common(100)

# Occurence of all the clean words (approximate number by trial and error)
clean_words_occ = Counter(" ".join(clean_data['Abstract']).split()).most_common(2900)

# Number of articles that write about 1 subject AND/OR another
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
def nb_art_vs_2sub(word1, word2, df, col_words):
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
# Number of articles that write about micro AND/OR nano fibers
nb_art_fiber_size = nb_art_vs_2sub('microfib', 'nanofib', clean_data, 'Abstract')
# Number of articles that write about viscosity AND/OR solution
nb_art_visco_vs_sol = nb_art_vs_2sub('viscos', 'solut', clean_data, 'Abstract')

# Most common bigrams and trigrams in clean data
# Puting all abstracts into a list
all_abstracts_list = clean_data['Abstract'].tolist()
# Defining variables
all_abstracts_bigrams = []
all_abstracts_trigrams = []
# Creating list of bigrams and trigrams by abstracts, i.e. list[0]=allBigramOfAbs1
for abstracts in all_abstracts_list:
    abstracts = word_tokenize(abstracts)
    all_abstracts_bigrams.append(list(bigrams(abstracts)))
    all_abstracts_trigrams.append(list(trigrams(abstracts)))
# Obtaining the most commons ones by abstracts for all of them
top3_bi = []
for bi_by_abst in all_abstracts_bigrams:
    top3_bi_by_abst = Counter(bi_by_abst).most_common(3)
    top3_bi.append(top3_bi_by_abst)
top3_tri = []
for tri_by_abst in all_abstracts_trigrams:
    top3_tri_by_abst = Counter(tri_by_abst).most_common(3)
    top3_tri.append(top3_tri_by_abst)

# Most common author's full name
top_authors = Counter(" ".join(clean_data['Author Full Names']).split('-')).most_common(10)

# Score
"""
Sorting the articles with the help of an homemade intuition base criteria's equation
-1 : solut, tio, carbon, tissu, cell, drug, treatment, scaffold, less than 10 citations
+1 : microfib, most common authors, jet, model, nozzle, temperatur, morpholog, speed, viscos
"""
# Definition of constants and variables
clean_data['Score'] = 0
minus_word = ['solut', 'tio', 'carbon', 'tissu', 'cell', 'drug', 'treatment', 'scaffold']
plus_word = ['microfib', 'jet', 'model', 'nozzl', 'temperatur', 'morpholog', 'speed', 'viscos']
cita_lim = 10
abst_words_by_art = []
authors_by_art = []
top_authors_list = []
i = -1
"""
Convert the list of single string into a list of multiple strings representing 
words (not the whole abstract)
"""
for abstracts in all_abstracts_list:
    abst_words_by_art.append(abstracts.split())
# Removing points depending of words that we don't particularly want into the article
for abstracts in abst_words_by_art:
    i += 1
    for word in minus_word:
        if word in abstracts:
           clean_data.at[i, 'Score'] -= 1
# =============================================================================
# # Reinitializing the indice and removing points depending of number of citations
# i = -1
# # Removing points if the article have been cite less than 10 times
# for nb_cita in clean_data['Total Citations']:
#     i += 1
#     if nb_cita < cita_lim:
#         clean_data.at[i, 'Score'] -= 1
# =============================================================================
# Reinitializing the indice and adding points depending of wanted words
i = -1
for abstracts in abst_words_by_art:
    i += 1
    for word in plus_word:
        if word in abstracts:
           clean_data.at[i, 'Score'] += 1
# =============================================================================
# """
# Convert the list of single string into a list of multiple strings representing 
# authors
# """           
# for author in clean_data['Author Full Names']:
#     authors_by_art.append(author.replace(" ", "").split('-'))
# # Convert the most common authors list of tuple into list of listed name
# for aut_tuple in top_authors:
#     top_authors_list.append(aut_tuple[0].replace(" ", ""))
# # Reinitializing the indice
# i = -1
# # Adding points if the article is written by anyone in the top 10 of most common authors
# for authors in authors_by_art:
#     i += 1
#     for name in top_authors_list:
#         if name in authors:
#            clean_data.at[i, 'Score'] += 1
#            
# =============================================================================
# =============================================================================
# # Plot
# # Creating histogram of number of articles in function of publication year
# nb_art_by_pub_year = clean_data['Publication Year'].replace('NaN', 0).value_counts().sort_index()
# nb_art_by_pub_year = pd.DataFrame(nb_art_by_pub_year)
# plt.bar(nb_art_by_pub_year.index.map(int).map(str), nb_art_by_pub_year['Publication Year'])
# plt.xticks(rotation = 65)
# plt.xlabel('Publication Year')
# plt.gcf().subplots_adjust(bottom=0.20)
# plt.ylabel('Number of Article')
# plt.suptitle('Number of articles by publication year')
# plt.savefig('./Results/PlotArticleByYear.svg')
# # Creating histogram of most common words in function of publication year?????? 100*25!!!!!!!!!!
# """
# Defining a function that create an histogram of number of articles mentioning a 
# certain clean word by publication year.
# Note : this function replace NaN made into 'NaN' to 0.
# Input :     word        word that is want to count by year (List of one string element)
#             df          dataframe that contain the two columns
#             col_word    column's name of the dataframe where to search the word (String)
#             col_year    column's name of the dataframe where it is store the year of publication (String)
#             plot_title  Title of the plot (String)
#             path        Where to save the plot (String)
# Return :    nb_word_by_year     
# Save :      plot bar (x,y) → (Publication Year, number of article)
# """
# def plot_word_by_year(word, df, col_word, col_year, path):
#     # Import
#     import matplotlib.pyplot as plt
#     import math
#     # Adding a new columns in df and if word in it put True un cell, else False
#     df['Word'] = df[col_word].apply(lambda x: any([k in x for k in word]))
#     # Creating a new datafram with the pub year columns and removing 'NaN' → all int
#     col_year_noStr = pd.DataFrame(df[col_year].replace('NaN', 0))
#     # Getting the publication year without duplicates as an index
#     nb_art_by_year = col_year_noStr.value_counts().sort_index()
#     nb_art_by_year = pd.DataFrame(nb_art_by_year)
#     # Creating a list from the index that have the years without duplicates
#     pub_year = pd.DataFrame(nb_art_by_year).index.sort_values().tolist()
#     # Creating a dataframe with two columns (year, count), count inisialize at 0
#     nb_word_by_year = pd.DataFrame(pub_year, columns=['Publication Year'])
#     nb_word_by_year['Count'] = 0
#     # Initializing the loop and counting nb of instance of the word by year
#     i = -1
#     for article in df[col_year]:
#         i += 1
#         j = -1
#         for year in nb_word_by_year['Publication Year']:     
#             j += 1
#             if (df.at[i, 'Word'] == True) & (col_year_noStr.at[i, col_year] == year):
#                 nb_word_by_year.at[j, 'Count'] += 1
#     # Removing the columns with the true or false indicating if the word is in it
#     del df['Word']
#     # Converting the year (int) into str in the dataframe used to plot → no bar 
#     # in year with no pub : so 0-2000 is not a problem
#     nb_word_by_year['Publication Year'] = nb_word_by_year['Publication Year'].astype(int).astype(str)
#     # Plotting the dataframe dans saving it in a folder
#     fig = plt.figure()
#     axes = fig.add_subplot()
#     axes.bar(nb_word_by_year['Publication Year'], nb_word_by_year['Count'], color = 'orchid')
#     axes.set_xlabel('Publication Year')
#     axes.set_ylabel('Number of article with ' + word[0])
#     axes.set_title('Number of article mentionning ' + word[0] + ' by year')
#     plt.xticks(rotation = 65)
#     min_y = min(nb_word_by_year['Count'])
#     max_y = max(nb_word_by_year['Count'])
#     y_increment_by_1 = range(math.floor(min_y), math.ceil(max_y)+1)
#     plt.yticks(y_increment_by_1)
#     plt.gcf().subplots_adjust(bottom=0.20)
#     plt.savefig(path)
#     # Return the dataframe
#     return nb_word_by_year
# # Creating histogram of number of articles mentioning microfib in function of publication year
# plot_word_by_year(['microfib'], clean_data, 'Abstract', 'Publication Year', './Results/PlotMicrofibByYear.svg')
# # Creating histogram of number of articles mentioning scaffold in function of publication year
# plot_word_by_year(['scaffold'], clean_data, 'Abstract', 'Publication Year', './Results/PlotScaffoldByYear.svg')
# # Creating histogram of number of articles mentioning viscos in function of publication year
# plot_word_by_year(['viscos'], clean_data, 'Abstract', 'Publication Year', './Results/PlotViscosByYear.svg')
# 
# 
# 
# # Write files
# # If there is no folder for the result create one
# os.makedirs('Results', exist_ok=True)
# 
# # Writing a csv file for the occurence of all the clean words
# clean_words_occ_df = pd.DataFrame(clean_words_occ, columns=['Word', 'Count'])
# clean_words_occ_df.to_csv('./Results/CleanWordsOccurence.csv', sep=';')
# =============================================================================

# Writing a csv file with the article sorted by the score
# Creating a refined dataframe
art_refined_by_score = pd.concat([clean_data['Score'], raw_data_useField['Article Title'], clean_data['UT (Unique WOS ID)']], axis=1)
art_sorted_by_score_df = pd.DataFrame(art_refined_by_score).sort_values(by='Score', ascending=False)
# Writing the file
art_sorted_by_score_df.to_csv('./Results/ArticlesSortedByScore.csv', sep=';')
