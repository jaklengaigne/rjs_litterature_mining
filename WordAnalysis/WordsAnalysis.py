"""
Base on this tutorial
Chalaguine, L. A. (2020, August 3). Getting started with text analysis in Python. Medium. https://towardsdatascience.com/getting-started-with-text-analysis-in-python-ca13590eb4f7
"""

# Librairies 
import pandas as pd
import warnings
import re
from nltk.stem import WordNetLemmatizer, PorterStemmer, SnowballStemmer
from nltk import word_tokenize, bigrams, trigrams
from collections import Counter
import os



# Do not know why
#warnings.filterwarnings('ignore')



# Read the database file
raw_data = pd.read_csv("DataBase_20210503.csv", sep=";")



# Return the data frame of raw_data
raw_data.head
#print(raw_data.head)



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
#print(raw_data_useField)



# Changing the type of NaN to string (For text cleaning everything need to be string)
raw_data_str = raw_data_useField.fillna("NaN")



# Text cleaning (removal of "meaningless" words)
"""
SmartStoplist.txt
by Lisa Andreevna
Lisanka93/text_analysis_python_101. (n.d.). GitHub. Retrieved May 3, 2021, from https://github.com/lisanka93/text_analysis_python_101
**** Note : nan is added to Lisa Andreevna's list ****
"""
# Definition of constant and variable
stop_words_file = 'SmartStoplist.txt'
stop_words = []
# Do not understand yet
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
#print(top_hundred)
# Occurence of all the clean words (approximate number by trial and error)
clean_words_occ = Counter(" ".join(clean_data['Abstract']).split()).most_common(2900)
#print(clean_words_occ)

# Number of articles that write about micro AND/OR nano fibers
# Defining the works to look for
microfib_word = ['microfib']
nanofib_word = ['nanofib']
# Adding columns 'Micro' and 'Nano'. Putting True in according cell if word is found.
clean_data['Micro'] = clean_data['Abstract'].apply(lambda x: any([k in x for k in microfib_word]))
clean_data['Nano'] = clean_data['Abstract'].apply(lambda x: any([k in x for k in nanofib_word]))
# Adding column to check if an article write about both, if so put True in the cell
clean_data['Micro and nano'] = (clean_data['Micro'] == True) & (clean_data['Nano'] == True)
#print(clean_data)
# Counting the number of true for each new columns
# one method
micro_art = clean_data.value_counts('Micro').loc[True]
# other method
nano_art = clean_data['Nano'].sum()
micro_nano_art = clean_data['Micro and nano'].sum()
# Creating a dataframe with those information
nb_art_fiber_size = {'Occurence': [micro_art, nano_art, micro_nano_art]}
nb_art_fiber_size_df = pd.DataFrame(nb_art_fiber_size, index=['Micro', 'Nano', 'Both'])
# Deleting all the new columns because this particular analyse is done
del clean_data['Micro']
del clean_data['Nano']
del clean_data['Micro and nano']

# Copy paste of section just above, I shoul write a function for this because that's bad
# Number of articles that write about viscosity AND/OR solution
# Defining the works to look for
visco_word = ['viscos']
sol_word = ['solut']
# Adding columns 'Micro' and 'Nano'. Putting True in according cell if word is found.
clean_data['Viscosity'] = clean_data['Abstract'].apply(lambda x: any([k in x for k in visco_word]))
clean_data['Solution'] = clean_data['Abstract'].apply(lambda x: any([k in x for k in sol_word]))
# Adding column to check if an article write about both, if so put True in the cell
clean_data['Both'] = (clean_data['Viscosity'] == True) & (clean_data['Solution'] == True)
#print(clean_data)
# Counting the number of true for each new columns
# one method
visco_art = clean_data.value_counts('Viscosity').loc[True]
# other method
sol_art = clean_data['Solution'].sum()
visco_sol_art = clean_data['Both'].sum()
# Creating a dataframe with those information
nb_art_visco_of_sol = {'Occurence': [visco_art, sol_art, visco_sol_art]}
nb_art_visco_of_sol_df = pd.DataFrame(nb_art_visco_of_sol, index=['Viscosity', 'Solution', 'Both'])
# Deleting all the new columns because this particular analyse is done
del clean_data['Viscosity']
del clean_data['Solution']
del clean_data['Both']

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
"""
Convert the list of single string into a list of multiple strings representing 
authors
"""           
for author in clean_data['Author Full Names']:
    authors_by_art.append(author.replace(" ", "").split('-'))
# Convert the most common authors list of tuple into list of listed name
for aut_tuple in top_authors:
    top_authors_list.append(aut_tuple[0].replace(" ", ""))
# Reinitializing the indice
i = -1
# Adding points if the article is written by anyone in the top 10 of most common authors
for authors in authors_by_art:
    i += 1
    for name in top_authors_list:
        if name in authors:
           clean_data.at[i, 'Score'] += 1



# Write files
# If there is no folder for the result create one
os.makedirs('Results', exist_ok=True)

# Writing a csv file for the occurence of all the clean words
clean_words_occ_df = pd.DataFrame(clean_words_occ, columns=['Word', 'Count'])
clean_words_occ_df.to_csv('./Results/CleanWordsOccurence.csv', sep=';')

# Writing a csv file for 