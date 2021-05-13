# -*- coding: utf-8 -*-
"""
Created on Thu May 13 09:22:05 2021

@author: Valérie Toupin-Guay
"""
import pandas as pd

word = ['Prout']
d = {'A': ['ish', 'Prout', 'bird', 'Prout', 'Prout'], 'B': [2003, 2004, 2004, 1999, 2004]}
df = pd.DataFrame(d)
col_word = 'A'
col_year = 'B'
plot_title = ' Nb of worb by year'
path = './TestPlot/figTest1.svg'

def plot_word_by_year(word, df, col_word, col_year, plot_title, path):
    import matplotlib.pyplot as plt
    df['Word'] = df[col_word].apply(lambda x: any([k in x for k in word]))
    nb_art_by_year = df[col_year].replace('NaN', 0).value_counts()
    nb_art_by_year.sort_index()
    pub_year = pd.DataFrame(nb_art_by_year).index.sort_values().tolist()
    nb_word_by_year = pd.DataFrame(pub_year, columns=['Publication Year'])
    nb_word_by_year['Count'] = 0
    i = -1
    for article in df[col_year]:
        i += 1
        j = -1
        for year in nb_word_by_year['Publication Year']:     
            j += 1
            if (df.at[i, 'Word'] == True) & (df.at[i, 'B'] == year):
                nb_word_by_year.at[j, 'Count'] += 1
    del df['Word']
    plt.bar(nb_word_by_year['Publication Year'], nb_word_by_year['Count'])
    plt.suptitle(plot_title)
    plt.savefig(path)
    return nb_word_by_year

plot_word_by_year(word, df, col_word, col_year, plot_title, path)