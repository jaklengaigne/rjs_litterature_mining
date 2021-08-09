import numpy as np 
import operator

#***************************************************************************
'''
To sort in the function I need to return a new dataFrame and it seem
to not work properly when I call twice the function???? To investigate
So I decided to only score and not sort in the function :(
'''
#***************************************************************************

# Score
"""
Scoring the articles with the help of an homemade intuition base criteria's equation
There is two main way to use this function. You can search if the text contain
some specifics words or you can check if a numeric parameter respect a certain
condition. You can also use both at the same time. If you choose to work with
words then you need to call as parameter : df, lst_word, lst_score and col_word.
If you choose to work with numeric then you need to call as parameter : df and
col_num (condition can be change but has a default state). The function added
a column score to the original dataframe (df) then you can refined and ordered
by score your dataframe. The function can be use twice or more. The score is
cumulative, in other word the function check if the column Score is existing.
    Input :     df          dataframe that contain the columns (see below)
                lst_word    list of words to search in text (List of strings)
                            Default=None
                lst_score   list of score associate with the words (List of integer)
                            Default=None
                col_word    column's name of the dataframe where to search words (String)
                            Default=None
                limit       second term in comparison expression, limiting number (Numeric)
                            Default=None
                col_num     column's name than contain the first term in comparison expression (String)
                            Default=None
                condition   python comparision operator as '==' ('String')
                            Default='<'
    Return :    Nothing, it modified the original df
"""
def sorted_by_score(df, lst_word=None, lst_score=None, col_word=None, limit=None, col_num=None, condition='<'):
    # Definition of constants and variables
    try:
        df['Score'][1]
    except:
        df['Score'] = 0
    ops = {
    '<' : operator.lt,
    '<=' : operator.le,
    '==' : operator.eq,
    '!=' : operator.ne,
    '>=' : operator.ge,
    '>' : operator.gt,
    }       
    if col_word is not None:
        abst_words_by_art = []
        i = -1
        # Convert the list of single string into a list of multiple strings representing
        # words (not the whole abstract)
        all_abstracts_list = df[col_word].tolist()
        for abstracts in all_abstracts_list:
            if abstracts is not np.nan:
                abst_words_by_art.append(abstracts.split())
            else:
                abst_words_by_art.append(abstracts)
        # Removing-adding points depending of words
        for abstracts in abst_words_by_art:
            i += 1
            if abstracts is not np.nan:
                for j in range(len(lst_word)):
                    if lst_word[j] in abstracts:
                        df.at[i, 'Score'] += lst_score[j]
    if col_num is not None:
        # Reinitializing the indice and removing points depending of number
        i = -1
        # Adding points according to condition and limit
        for nb_cita in df[col_num]:
            i += 1
            if ops[condition](nb_cita, limit):
                df.at[i, 'Score'] += 1



import pandas as pd

# 1) big lists    
df_test1 = pd.read_csv('../WordAnalysis/DataBase_20210522.csv', sep=';')
dict_word1 = {'word':['solution', 'tio', 'carbon', 'tissue', 'cellular', 'drug', 
                     'treatment', 'scaffold', 'microfiber', 'jet', 'model',
                     'nozzle', 'temperature', 'morphology', 'speed', 'viscosity'],
             'score':[-1, -2, -2, -2, -3, -3, -1, -2, 2, 1, 1, 2, 3, 2, 2, 3]
             }
df_ref1 = pd.DataFrame(dict_word1)
sorted_by_score(df_test1, df_ref1['word'], df_ref1['score'], 'Abstract')

# 2) easy to spot mistakes → ok
df_test2 = pd.read_csv('../WordAnalysis/DataBase_20210522.csv', sep=';')
dict_word2 = {'word':['solution',
                     'nozzle'],
             'score':[-1, 1]
             }
df_ref2 = pd.DataFrame(dict_word2)
sorted_by_score(df_test2, df_ref2['word'], df_ref2['score'], 'Abstract')

# 3) function use twice → ok
df_test3 = pd.read_csv('../WordAnalysis/DataBase_20210522.csv', sep=';')
sorted_by_score(df_test3, df_ref2['word'], df_ref2['score'], 'Abstract')
sorted_by_score(df_test3, df_ref2['word'], df_ref2['score'], 'Abstract')

# 4) function both word-num → ok
df_test4 = pd.read_csv('../WordAnalysis/DataBase_20210522.csv', sep=';')
sorted_by_score(df_test4, df_ref2['word'], df_ref2['score'], 'Abstract', 10, 'Times Cited, All Databases')

# 5) function with only num → ok
df_test5 = pd.read_csv('../WordAnalysis/DataBase_20210522.csv', sep=';')
sorted_by_score(df_test5, limit=(10), col_num=('Times Cited, All Databases'))

# 6) function with only num, change comparison operator → ok!
df_test6 = pd.read_csv('../WordAnalysis/DataBase_20210522.csv', sep=';')
sorted_by_score(df_test6, limit=(1), col_num=('Times Cited, All Databases'), condition='==')

'''
To sort in the function I need to return a new dataFrame and it seem
to not work properly when I call twice the function???? To investigate
'''
df_test3m = df_test3.sort_values(by='Score', ascending=False)

# Help
'''
PaulMcG. (n.d.). python—Turn string into operator. Stack Overflow.
Retrieved August 8, 2021, from https://stackoverflow.com/questions/1740726/turn-string-into-operator
'''

