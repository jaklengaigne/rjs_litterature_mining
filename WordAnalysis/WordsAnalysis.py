"""
Based on this tutorial
Lisanka93/text_analysis_python_101. (n.d.). GitHub.
Retrieved May 3, 2021, from
https://github.com/lisanka93/text_analysis_python_101/blob/master/Railroad_incidents_USA2019.ipynb
"""

# Librairies
import pandas as pd
from nltk import word_tokenize, bigrams, trigrams
from collections import Counter
import os
import matplotlib.pyplot as plt
import wordanalysis as wa



# Read the database file
raw_data = pd.read_csv("DataBase_20210522.csv", sep=";")



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
raw_data_noDup = raw_data[raw_data['dup'] == False]
"""
Deleting the column with the True and False because because it is
no more useful
"""
del raw_data_noDup['dup']



# Removing useless columns (All articles have written nothing in those fields)
raw_data_useField = raw_data_noDup.dropna(axis=1, how='all')



# Changing the type of NaN to string
# (For text cleaning everything need to be string)
raw_data_str = raw_data_useField.fillna("NaN")



# Text cleaning (removal of "meaningless" words)
# Clean abstracts of all the articles of the research (overwrite)
raw_data_str['Abstract'] = wa.preprocess(raw_data_str['Abstract'], 'SmartStoplist.txt')
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
# Number of articles that write about micro AND/OR nano fibers
nb_art_fiber_size = wa.nb_art_vs_2sub('microfib', 'nanofib', clean_data, 'Abstract')
# Number of articles that write about viscosity AND/OR solution
nb_art_visco_vs_sol = wa.nb_art_vs_2sub('viscos', 'solut', clean_data, 'Abstract')

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
+1 : microfib, jet, model, nozzle, temperatur, morpholog, speed, viscos
"""
# Definition of constants and variables
clean_data['Score'] = 0
minus_word = ['solut', 'tio', 'carbon', 'tissu', 'cell', 'drug', 'treatment', 'scaffold']
plus_word = ['microfib', 'jet', 'model', 'nozzl', 'temperatur', 'morpholog', 'speed', 'viscos']
cita_lim = 10
abst_words_by_art = []
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
# Reinitializing the indice and removing points depending of number of citations
i = -1
# Removing points if the article have been cite less than 10 times
for nb_cita in clean_data['Total Citations']:
    i += 1
    if nb_cita < cita_lim:
        clean_data.at[i, 'Score'] -= 1
# Reinitializing the indice and adding points depending of wanted words
i = -1
for abstracts in abst_words_by_art:
    i += 1
    for word in plus_word:
        if word in abstracts:
            clean_data.at[i, 'Score'] += 1

# Most common materials
# First a materials columns was manually add in CleanWordsOccurence.csv and fill
# with 1 if the word was a material
clean_words_occ_dfm = pd.read_csv("CleanWordsOccurence_modified.csv", sep=",")
clean_words_occ_dfm = clean_words_occ_dfm.fillna('nan')
material_df = clean_words_occ_dfm[clean_words_occ_dfm.materials != 'nan']

# Articles mentionning a certain word
# Articles about blend material
art_with_blend = wa.article_with_word('blend', clean_data, 'Abstract', 'Article Title', 'UT (Unique WOS ID)')

# Article in a journal with a country or city in his name (might be use in futur to remove point from score)

# Keyword comparison with research areas (most tuple → (keyw, rea) as bigrams)

# average number of page by document type plot

# number of page vs cited reference count

# map author from addresses



# Plot
# Creating histogram of number of articles in function of publication year
nb_art_by_pub_year = clean_data['Publication Year'].replace('NaN', 0).value_counts().sort_index()
nb_art_by_pub_year = pd.DataFrame(nb_art_by_pub_year)
plt.bar(nb_art_by_pub_year.index.map(int).map(str), nb_art_by_pub_year['Publication Year'])
plt.xticks(rotation=65)
plt.xlabel('Publication Year')
plt.gcf().subplots_adjust(bottom=0.20)
plt.ylabel('Number of Article')
plt.suptitle('Number of articles by publication year')
plt.savefig('./Results/PlotArticleByYear.svg')
# Creating histogram of number of articles mentioning microfib in function of publication year
wa.plot_word_by_year(['microfib'], clean_data, 'Abstract', 'Publication Year', './Results/PlotMicrofibByYear.svg')
# Creating histogram of number of articles mentioning scaffold in function of publication year
wa.plot_word_by_year(['scaffold'], clean_data, 'Abstract', 'Publication Year', './Results/PlotScaffoldByYear.svg')
# Creating histogram of number of articles mentioning viscos in function of publication year
wa.plot_word_by_year(['viscos'], clean_data, 'Abstract', 'Publication Year', './Results/PlotViscosByYear.svg')

# Map of publisher's city
wa.map_publisher_city(clean_data, 'Publisher City', './Results/mapPublisherCity.html')



# Write files
# If there is no folder for the result create one
os.makedirs('Results', exist_ok=True)

# Writing a csv file for the occurence of all the clean words
clean_words_occ_df = pd.DataFrame(clean_words_occ, columns=['Word', 'Count'])
clean_words_occ_df.to_csv('./Results/CleanWordsOccurence.csv', sep=';')

# Writing a csv file with the article sorted by the score
# Creating a refined dataframe
art_refined_by_score = pd.concat([clean_data['Score'], raw_data_useField['Article Title'], clean_data['UT (Unique WOS ID)']], axis=1)
art_sorted_by_score_df = pd.DataFrame(art_refined_by_score).sort_values(by='Score', ascending=False)
# Writing the file
art_sorted_by_score_df.to_csv('./Results/ArticlesSortedByScore.csv', sep=';')

# Writing a csv file with the mention materials sorted by most common
material_df.to_csv('./Results/MaterialsSortedByMostCommon.csv', sep=';')

# Writing a csv file with articles about blend material
art_with_blend.to_csv('./Results/ArticlesAboutBlend.csv', sep=';')