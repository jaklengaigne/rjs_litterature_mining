# -*- coding: utf-8 -*-
"""
Created on Tue May 18 15:09:34 2021

@author: Valérie Toupin-Guay
"""

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

import pandas as pd


def article_with_word(word, df, col_word, col_info, col_ID):
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

ad = {'A': ['wow un pissenlit', 'choucroute', 'bird oiseau', 'NaN', 'choucroute de pissenlit'], 
      'B': ['nan', 1, 2, 'NaN', 4], 
      'C': ['I am here ', 'chauve-souris', 'nan', 'NaN', '123']}
adf = pd.DataFrame(ad)
aword = 'choucroute'
acol_word = 'A'
acol_info = 'C'
acol_ID = 'B'

test1 = article_with_word(aword, adf, acol_word, acol_info, acol_ID)



bd = {'rosemary': ['Alice', 'Charles', 'Antoine', 'Valérie', 'Naeige'], 
      'adresse': [1080, 1, 20, 0, 'ut-f 2823189231723'], 
      'bleu lavande': ['bleu', 'rouge', 'rose', 'orange', 'vert']}
bdf = pd.DataFrame(bd)
bword = 'Alice'
bcol_word = 'rosemary'
bcol_info = 'bleu lavande'
bcol_ID = 'adresse'

test2 = article_with_word(bword, bdf, bcol_word, bcol_info, bcol_ID)