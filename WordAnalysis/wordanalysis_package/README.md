# README

wordanalysis package contains all the functions used in the main program : [main_word_analysis.py](https://github.com/ets-lipec/rjs_litterature_mining/blob/convertopackage/WordAnalysis/main_words_analysis.py)

## Class and methods

* Process :
    * nb_art_vs_2sub(word1, word2, df, col_words)
    * article_with_word(word, df, col_word, col_info, col_ID)
    * most_common_bigrams(df, col_text, top_x)
    * most_common_trigrams(df, col_text, top_x)
    * plot_word_by_year(word, df, col_word, col_year, path)
    * nb_pub_by_year(df, col_year, path_svg)
    * map_publisher_city(df, col_city, path)
    * score(df, lst_word=None, lst_score=None, col_word=None, limit=None, col_num=None, condition='<')

* RawDf :
    * preprocess()

* RawTxt :
    * preprocess(stopwords_file, opt_caps='no', opt_stem='no')

* WOSdf

For more informations about those functions see there heading directly in [wordanalysis_package.py](https://github.com/jaklengaigne/rjs_litterature_mining/blob/main/WordAnalysis/wordanalysis/wordanalysis.py)