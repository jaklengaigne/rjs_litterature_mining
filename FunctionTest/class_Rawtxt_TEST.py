import re
from nltk.stem import PorterStemmer


class Rawtxt:
    # Constructor
    def __init__(self, raw_text):
        self.raw = raw_text
    # Methods
    # mutators
    
    # =============================================================================
    # SmartStoplist.txt
    # by Lisa Andreevna
    # Lisanka93/text_analysis_python_101. (n.d.). GitHub. Retrieved May 3, 2021,
    # from https://github.com/lisanka93/text_analysis_python_101
    # **** Note : nan is added to Lisa Andreevna's list ****
    # =============================================================================
    """
    Definition of a cleaning function (preprocess before words analysis)
    This function get a text, the name of a stop words list and ask for
    two options : if you want to have a text in capitals and if you want
    to stem the words.
    If all options are chosen than the function return a text (string) of
    stemmed word in capitals without stop words and any caracter except letter.
    Input :     raw_text        text to be clean (String)
                stopwords_file  name.txt of file that contains list of stop words
                                (String) Need to be in the same folder as raw_text
                opt_caps        Default='no', opt_caps='yes' → clean text in capitals
                opt_stem        Default='no', opt_stem='yes' → clean text with stem words
    Return :    clean_text      raw_text without special caracter and stop words, 
                                in lowercase with only stemmed words
    """
    def preprocess(self, stopwords_file, opt_caps='no', opt_stem='no'):
        # Definition of constant and variable
        stop_words_file = stopwords_file
        stop_words = []
        # Creating a list of stop words while reading the stop words's file
        with open(stop_words_file, "r") as f:
            for line in f:
                stop_words.extend(line.split())
        stop_words = stop_words
        # Replace letter with ornament
        no_acccent = self.raw.upper().replace("À","A").replace("Â","A").replace("Á", "A").replace("Ä","A").replace("Ã","A").replace("Ā","A").replace("Ą","A").replace("È","E").replace("Ê","E").replace("É","E").replace("Ë","E").replace("Ẽ","E").replace("Ę","E").replace("Ì","I").replace("Î","I").replace("Í","I").replace("Ï","I").replace("Ĩ","I").replace("Ī","I").replace("Ò","O").replace("Ô","O").replace("Ó", "O").replace("Ö","O").replace("Õ","O").replace("Ō","O").replace("Ù","U").replace("Û","U").replace("Ú", "U").replace("Ü","U").replace("Ũ","U").replace("Ū","U").replace("Ç", "C").replace("Ḏ","D").replace("Ń","N").replace("Ñ", "N").replace("Ś","S").replace("Ş","S").replace("Ź","Z").replace("Ż","Z").replace("Ţ","T").replace("Ł","T").replace("–", "-").replace("-", " ").replace("’", " ").replace("‘"," ").replace("'", " ").replace("̧ "," ").replace(".", "").replace("  "," ")
        # Keep only letters and cut the text (str) into words (list of str)
        words = re.sub("[^a-zA-Z]", " ", no_acccent).lower().split()
        # Define a variable to receive only the useful crop (or not) words
        cleaned_words = []
        # Remove stop words
        for word in words:
            if word not in stop_words:
                cleaned_words.append(word)
        if opt_stem == 'yes':
            # Stem word
            stemmed_words = []
            for word in cleaned_words:
                word = PorterStemmer().stem(word)
                stemmed_words.append(word)
            if opt_caps == 'yes':
                # Change the lowercase for uppercase
                return " ".join(stemmed_words).upper()
            else:
                # After all those changes, convert back the final list into string
                return " ".join(stemmed_words)
        else:
            if opt_caps == 'yes':
                # Change the lowercase for uppercase
                return " ".join(cleaned_words).upper()
            else:
                return " ".join(cleaned_words).lower()
    
monTexte = 'J\'écris 1.0 texte poUr le TESTER à 100 % and to be PLEASE 5:5\n Amusing!'
obj1 = Rawtxt(monTexte)
test1 = obj1.preprocess('SmartStoplist.txt', 'yes', 'yes')

obj2 = Rawtxt(monTexte)
test2 = obj2.preprocess('SmartStoplist.txt', 'lowercase', 'yes')

obj3 = Rawtxt(monTexte)
test3 = obj3.preprocess('SmartStoplist.txt', 'lowercase', 'not stem')

obj4 = Rawtxt(monTexte)
test4 = obj4.preprocess('SmartStoplist.txt')



