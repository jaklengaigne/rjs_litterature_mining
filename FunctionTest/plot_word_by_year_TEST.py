# -*- coding: utf-8 -*-
"""
Created on Thu May 13 09:22:05 2021

@author: Valérie Toupin-Guay
"""
import pandas as pd

def plot_word_by_year(word, df, col_word, col_year, plot_title, path):
    import matplotlib.pyplot as plt
    import math
    
    df['Word'] = df[col_word].apply(lambda x: any([k in x for k in word]))
    col_year_noStr = pd.DataFrame(df[col_year].replace('NaN', 0))
    nb_art_by_year = col_year_noStr.value_counts().sort_index()
    nb_art_by_year = pd.DataFrame(nb_art_by_year)
    pub_year = pd.DataFrame(nb_art_by_year).index.sort_values().tolist()
    nb_word_by_year = pd.DataFrame(pub_year, columns=['Publication Year'])
    nb_word_by_year['Count'] = 0
    i = -1
    for article in df[col_year]:
        i += 1
        j = -1
        for year in nb_word_by_year['Publication Year']:     
            j += 1
            if (df.at[i, 'Word'] == True) & (col_year_noStr.at[i, col_year] == year):
                nb_word_by_year.at[j, 'Count'] += 1
    del df['Word']
    nb_word_by_year['Publication Year'] = nb_word_by_year['Publication Year'].astype(str)
    
    fig = plt.figure()
    axes = fig.add_subplot()
    axes.bar(nb_word_by_year['Publication Year'], nb_word_by_year['Count'], color = 'orchid')
    axes.set_xlabel('Publication Year')
    axes.set_ylabel('Number of article with ' + word[0])
    axes.set_title(plot_title)
    plt.xticks(rotation = 65)
    min_y = min(nb_word_by_year['Count'])
    max_y = max(nb_word_by_year['Count'])
    y_increment_by_1 = range(math.floor(min_y), math.ceil(max_y)+1)
    plt.yticks(y_increment_by_1)
    plt.gcf().subplots_adjust(bottom=0.20)
    plt.savefig(path)
    return nb_word_by_year

# Test 1
word = ['Prout']
d = {'A': ['ish', 'Prout', 'lie', 'Prout', 'bird', 'Prout'], 'B': [2003, 0, 2004, 2004, 1999, 2004]}
df = pd.DataFrame(d)
col_word = 'A'
col_year = 'B'
plot_title = ' Nb of word by year'
path = './TestPlot/figTest1.svg'

test1 = plot_word_by_year(word, df, col_word, col_year, plot_title, path)

# Test 2
word = ['cheval']
d = {'Rasta': ['cheval', 'arc', 'bee', 'fleur', 'flash', 'cheval'], 'Germe': [2004, 2021, 2004, 2004, 1999, 'NaN']}
df = pd.DataFrame(d)
col_word = 'Rasta'
col_year = 'Germe'
plot_title = ' Nb of word by year'
path = './TestPlot/figTest2.svg'

test2 = plot_word_by_year(word, df, col_word, col_year, plot_title, path)

# Test 3
word = ['a']
d = {'123': ['a', 'a', 'a', 'a', 'a', 'b'], '456': [56, 99, 56, 56, 56, 56]}
df = pd.DataFrame(d)
col_word = '123'
col_year = '456'
plot_title = ' Nb of word by year'
path = './TestPlot/figTest3.svg'

test3 = plot_word_by_year(word, df, col_word, col_year, plot_title, path)