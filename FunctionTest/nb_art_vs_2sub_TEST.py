# -*- coding: utf-8 -*-
"""
Created on Thu May 13 15:59:05 2021

@author: Valérie Toupin-Guay
"""

import pandas as pd

word1 = 'choucroute'
word2 = 'pissenlit'
d = {'A': ['wow un pissenlit', 'choucroute', 'bird oiseau', 'choucroute qui sent fort', 'choucroute de pissenlit'], 'B': [2003, 2004, 2004, 1999, 2004]}
df = pd.DataFrame(d)
col_words = 'A'

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

test = nb_art_vs_2sub(word1, word2, df, col_words)