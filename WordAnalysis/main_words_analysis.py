"""
Based on this tutorial
Lisanka93/text_analysis_python_101. (n.d.). GitHub.
Retrieved May 3, 2021, from
https://github.com/lisanka93/text_analysis_python_101/blob/master/Railroad_incidents_USA2019.ipynb
"""

# Librairies
import pandas as pd
from collections import Counter
import os
import wordanalysis as wa


# Read the database file
raw_data = pd.read_csv("DataBase_20210522.csv", sep=";")

# Return the data frame of raw_data
raw_data.head

# Simplified the data frame
raw_data_obj = wa.RawDf(raw_data)
raw_data_simplified = raw_data_obj.preprocess()


# Text cleaning (removal of "meaningless" words)
# Clean abstracts of all the articles of the research (overwrite)
for i, abstract in enumerate(raw_data_simplified['Abstract']):
    abstract = wa.RawTxt(abstract).preprocess('SmartStoplist.txt', opt_stem='yes')
    raw_data_simplified['Abstract'][i] = abstract
clean_data = raw_data_simplified

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
nb_art_fiber_size = wa.Process().nb_art_vs_2sub('microfib', 'nanofib', clean_data, 'Abstract')
# Number of articles that write about viscosity AND/OR solution
nb_art_visco_vs_sol = wa.Process().nb_art_vs_2sub('viscos', 'solut', clean_data, 'Abstract')

# Most common bigrams and trigrams in clean data
top3_bi = wa.Process().most_common_bigrams(clean_data, 'Abstract', 3)
top3_tri = wa.Process().most_common_trigrams(clean_data, 'Abstract', 3)

# Most common author's full name
top_authors = Counter(" ".join(clean_data['Author Full Names']).split('-')).most_common(10)

# Score
"""
Sorting the articles with the help of an homemade intuition base criteria's equation
-1 : solut, tio, carbon, tissu, cell, drug, treatment, scaffold, less than 10 citations
+1 : microfib, jet, model, nozzle, temperatur, morpholog, speed, viscos
"""
term = ['solut', 'tio', 'carbon', 'tissu', 'cell', 'drug', 'treatment', 'scaffold',
        'microfib', 'jet', 'model', 'nozzl', 'temperatur', 'morpholog', 'speed', 'viscos']
points = [-1, -1, -1, -1, -1, -1, -1, -1,
         1, 1, 1, 1, 1, 1, 1, 1]
cita_lim = 10
wa.Process().score(clean_data, term, points, 'Abstract', cita_lim, 'Total Citations', condition='>')

# Most common materials
# First a materials columns was manually add in CleanWordsOccurence.csv and fill
# with 1 if the word was a material
clean_words_occ_dfm = pd.read_csv("CleanWordsOccurence_modified.csv", sep=",")
clean_words_occ_dfm = clean_words_occ_dfm.fillna('nan')
material_df = clean_words_occ_dfm[clean_words_occ_dfm.materials != 'nan']

# Articles mentionning a certain word
# Articles about blend material
art_with_blend = wa.Process().article_with_word('blend', clean_data, 'Abstract', 'Article Title', 'UT (Unique WOS ID)')

# Article in a journal with a country or city in his name (might be use in futur to remove point from score)

# Keyword comparison with research areas (most tuple → (keyw, rea) as bigrams)

# average number of page by document type plot

# number of page vs cited reference count

# map author from addresses


# Plot
# Creating histogram of number of articles in function of publication year
wa.Process().nb_pub_by_year(clean_data, 'Publication Year', './Results/PlotArticleByYear.svg')
# Creating histogram of number of articles mentioning microfib in function of publication year
wa.Process().plot_word_by_year(['microfib'], clean_data, 'Abstract', 'Publication Year', './Results/PlotMicrofibByYear.svg')
# Creating histogram of number of articles mentioning scaffold in function of publication year
wa.Process().plot_word_by_year(['scaffold'], clean_data, 'Abstract', 'Publication Year', './Results/PlotScaffoldByYear.svg')
# Creating histogram of number of articles mentioning viscos in function of publication year
wa.Process().plot_word_by_year(['viscos'], clean_data, 'Abstract', 'Publication Year', './Results/PlotViscosByYear.svg')

# Map of publisher's city
wa.Process().map_publisher_city(clean_data, 'Publisher City', './Results/mapPublisherCity.html')


# Write files
# If there is no folder for the result create one
os.makedirs('Results', exist_ok=True)

# Writing a csv file for the occurence of all the clean words
clean_words_occ_df = pd.DataFrame(clean_words_occ, columns=['Word', 'Count'])
clean_words_occ_df.to_csv('./Results/CleanWordsOccurence.csv', sep=';')

# Writing a csv file with the article sorted by the score
# Creating a refined dataframe
art_refined_by_score = pd.concat([clean_data['Score'], raw_data_simplified['Article Title'], clean_data['UT (Unique WOS ID)']], axis=1)
art_sorted_by_score_df = pd.DataFrame(art_refined_by_score).sort_values(by='Score', ascending=False)
# Writing the file
art_sorted_by_score_df.to_csv('./Results/ArticlesSortedByScore.csv', sep=';')

# Writing a csv file with the mention materials sorted by most common
material_df.to_csv('./Results/MaterialsSortedByMostCommon.csv', sep=';')

# Writing a csv file with articles about blend material
art_with_blend.to_csv('./Results/ArticlesAboutBlend.csv', sep=';')
