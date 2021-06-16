# README

We mine text data extracted from the literature on rotary jet spinning published in scientific journals with the intent of guiding our research on the subject and find insight in the state of the art.

We first explore the data with a word analysis hoping that we could reduce the number of articles to data mined. We couldn't reduce it but we sorted them by giving subjective score to each article with some criteria easily manage in python code. Then we start datamining with those with the highest score.

The word analysis part is based on a railroad incident text analysis by Lisa Andreevna<sup id="a1">[1](#f1)</sup>. Also most of codes are in python but [map_of_publisher_cities](https://github.com/jaklengaigne/rjs_litterature_mining/blob/main/FunctionTest/map_of_publisher_cities_TEST.py), based on John Oh tutorial<sup id="a2">[2](#f2)</sup>, save to html to do world map.

## Data

* The first dataset originates from Web of Science database (https://apps.webofknowledge.com from Clariviate analytics) and contains all the bibliographic data from the keyword search:
TOPIC: ("rotary jet spinning"  OR "centrifugal spinning"  OR "cotton candy method") 
downloaded on: 2021-05 
For more information about how the exportation was carried out please go see this text file : [Exportation_Prepa_Of_RawDataBase.txt](https://github.com/jaklengaigne/rjs_litterature_mining/blob/main/WordAnalysis/Exportation_Prepa_Of_RawDataBase.txt)
The dataset use in [WordsAnalysis.py](https://github.com/jaklengaigne/rjs_litterature_mining/blob/main/WordAnalysis/WordsAnalysis.py) is contained here : [DataBase_20210522.csv](https://github.com/jaklengaigne/rjs_litterature_mining/blob/main/WordAnalysis/DataBase_20210522.csv)

## Main Folders

* [WordsAnalysis.py](https://github.com/jaklengaigne/rjs_litterature_mining/blob/main/WordAnalysis/WordsAnalysis.py) :
    * .txt : notes describing exportations
    * .xls : original file from exportation
    * .csv : modified files from exportation. used in .py
    * .py : main code
    * Exeptions :
        * [SmartStoplist.txt](https://github.com/jaklengaigne/rjs_litterature_mining/blob/main/WordAnalysis/SmartStoplist.txt) : contains stop words used to clean abstract's text in the database. This list originally was made by Lisa Andreevna<sup id="a3">[3](#f3)</sup> and the word nan was added to it
        * [Results](https://github.com/jaklengaigne/rjs_litterature_mining/tree/main/WordAnalysis/Results) : folder that contains all file made from [WordsAnalysis.py](https://github.com/jaklengaigne/rjs_litterature_mining/blob/main/WordAnalysis/WordsAnalysis.py)
        * [CleanWordsOccurence_modified.csv](https://github.com/jaklengaigne/rjs_litterature_mining/blob/main/WordAnalysis/CleanWordsOccurence_modified.csv) : manually modified file from the [Results](https://github.com/jaklengaigne/rjs_litterature_mining/tree/main/WordAnalysis/Results) folder that is passed a second time in the [WordsAnalysis.py](https://github.com/jaklengaigne/rjs_litterature_mining/blob/main/WordAnalysis/WordsAnalysis.py)
* [Datamining](https://github.com/jaklengaigne/rjs_litterature_mining/tree/main/DataMining) :
    * .yaml : data sheet template used to extract data from papers/articles
    * .csv : checklist to keep trace which articles have been data mined
    * [DataFileByArticles](https://github.com/jaklengaigne/rjs_litterature_mining/tree/main/DataMining/DataFileByArticles) : contains all the data sheet (one by article) and .txt files that explained how to proceed or where the notation comes from
* [FunctionTest](https://github.com/jaklengaigne/rjs_litterature_mining/tree/main/FunctionTest) : 
    * .py : contains tests of function used in [WordsAnalysis.py](https://github.com/jaklengaigne/rjs_litterature_mining/blob/main/WordAnalysis/WordsAnalysis.py) and [DataMining](https://github.com/jaklengaigne/rjs_litterature_mining/tree/main/DataMining)
    * .csv : related file needed to test [materials_table_TEST.py](https://github.com/jaklengaigne/rjs_litterature_mining/blob/main/FunctionTest/materials_table_TEST.py)
    * [TestPlot](https://github.com/jaklengaigne/rjs_litterature_mining/tree/main/FunctionTest/TestPlot) : contains resulting plot from tests

## Bibliographic References

[<b id="f1">1</b>] [↩](#a1) : Lisanka93/text_analysis_python_101. (n.d.). GitHub. Retrieved May 3, 2021, from https://github.com/lisanka93/text_analysis_python_101/blob/master/Railroad_incidents_USA2019.ipynb

[<b id="f2">2</b>] [↩](#a2) : Oh, J. (2020, April 23). Using Python to create a world map from a list of country names. Medium. https://towardsdatascience.com/using-python-to-create-a-world-map-from-a-list-of-country-names-cd7480d03b10

[<b id="f3">3</b>] [↩](#a3) : Lisanka93/text_analysis_python_101. (n.d.). GitHub. Retrieved May 3, 2021, from https://github.com/lisanka93/text_analysis_python_101/blob/master/SmartStoplist.txt