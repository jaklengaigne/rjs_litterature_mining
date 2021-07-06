import os
from bs4 import BeautifulSoup
import codecs
import re
import pandas as pd
import numpy as np
from nltk.stem import PorterStemmer


"""
Definition of a cleaning function (preprocess before words analysis)
This function get a text and file name containing a list of stop words. 
It return a text (string) of stemmed word inlowercase without stop words and 
any caracter except letter
"""
def preprocess(raw_text, stop_word_name_file):
    """
    SmartStoplist.txt
    by Lisa Andreevna
    Lisanka93/text_analysis_python_101. (n.d.). GitHub. Retrieved May 3, 2021,
    from https://github.com/lisanka93/text_analysis_python_101
    **** Note : nan is added to Lisa Andreevna's list ****
    """
    # Definition of constant and variable
    stop_words_file = stop_word_name_file
    stop_words = []
    # Creating a list of stop words while reading the stop words's file
    with open(stop_words_file, "r") as f:
        for line in f:
            stop_words.extend(line.split())
    stop_words = stop_words
    # Keep only letters in the text (lowercase and capitals) using Regex (re).
    # Replace all symboles with a blank space.
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


# Cleaned the materials reference list
# removed dupicated
ref = pd.read_csv('materials_list.csv', sep=";")
ref['dup'] = ref.duplicated(subset=None, keep='first')
ref['dup'].value_counts()
ref = ref[ref['dup'] == False]
del ref['dup']
ref = ref.dropna(axis=1, how='all').reset_index().drop('index', axis=1)
# preprocessed term as the document will be
clean_ref = ref.copy()
for i in range(len(clean_ref['Term'])):
    clean_ref['Term'][i] = preprocess(clean_ref['Term'][i], 'SmartStoplist.txt')
    clean_ref['Term'][i] = clean_ref['Term'][i].replace('plastic', '').replace('copolym', '').replace('resin', '').replace('comonom', '')
# removed cleaned term dupicated (keep most general abbreviation)
clean_ref['dup'] = clean_ref.duplicated(subset='Term', keep='first')
clean_ref['dup'].value_counts()
clean_ref = clean_ref[clean_ref['dup'] == False]
del clean_ref['dup']
clean_ref = clean_ref.dropna(axis=1, how='all').reset_index().drop('index', axis=1)


# Iterated throught a bunch of local html file
directory = './ArticlesHtml'
used_materials = pd.DataFrame()
for filename in os.listdir(directory):
    if filename.endswith('.html'):
        # Get article text from a saved html file
        path = os.path.join(directory, filename)
        f = codecs.open(path, 'r', 'utf-8')
        raw_document = BeautifulSoup(f.read(),features='html.parser').get_text()
        f.close()        
        # Cleaned the text
        # remove introduction and references
        rex_flush_intro = r'[\D][\.|\n](2\.?\s[A-Z]\w+)'
        header_after_intro = re.findall(rex_flush_intro, raw_document)
        if len(header_after_intro) == 1:
            raw_document = raw_document.split(header_after_intro[0])
            raw_document = raw_document[1]
        raw_document = raw_document.rsplit('References', 1)
        raw_document = raw_document[0]
        clean_doc = preprocess(raw_document, 'SmartStoplist.txt')
        # Search materials in text
        materials = pd.DataFrame()
        for term in clean_ref['Term']:
            if term in clean_doc:
                materials = materials.append([term])
        materials = materials.reset_index().drop('index', axis=1).transpose()
        if materials.empty:
            materials = [np.nan]
        used_materials = used_materials.append(materials)