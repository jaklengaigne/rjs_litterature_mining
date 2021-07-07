import os
from bs4 import BeautifulSoup
import codecs
import re
import pandas as pd
import numpy as np
import temp2temp as t2t

# Iterated throught a bunch of local html file
directory = './ArticlesHtml'
temp_range = pd.DataFrame(columns=('min', 'max'))
for filename in os.listdir(directory):
    if filename.endswith('.html'):
        # Get article text from a saved html file
        path = os.path.join(directory, filename)
        f = codecs.open(path, 'r', 'utf-8')
        document = BeautifulSoup(f.read(),features='html.parser').get_text()
        f.close()
        
        # Get tempmeter
        temp_rex = r'\s(\d{3,}\s?°?[CFK])[\s|\.]|\s(\d{3,}\s?±\s?\d{3,}\s?°?[CFK])[\s|\.]|\s(\d{3,}\s?\w+\s?\d{3,}\s?°?[CFK])[\s|\.]'
        temp = re.findall(temp_rex, document)
        
        # Keep only a range
        # clean tuple list of temp 
        # (remove empty string → false min, space, comma and untis → conversion)
        temp = [(re.split(' and | to | or |–|-| | | ', x) if isinstance(x, str) else x for x in _ if x) for _ in temp]
        # ((remove generator because it's painfull to work with as beginner in python))
        temp = pd.DataFrame(temp)
        if not temp.empty:
            temp = pd.DataFrame(temp[0].tolist())
            # ((change object type because everything is not suppose to be str))
            def isfloat(value):
              try:
                float(value)
                return True
              except ValueError:
                return False
            for i, row in temp.iterrows():
                for j in range(len(row)):
                    if isinstance(row[j], str):
                        if row[j].isdigit() or isfloat(row[j]):
                            row[j] = float(row[j])
                    if not row[j]:
                        row[j] = np.nan
            # ((special case : ±))
            bool_df = (temp == '±').any(axis=1)         
            for imatch in range(len(temp)):
                if bool_df[imatch]:
                    plus = temp.at[imatch, 0] + temp.at[imatch, 2]
                    new_rowp = [plus, temp.at[imatch, 3]]
                    new_rowp = pd.DataFrame(new_rowp).transpose()
                    
                    minus = temp.at[imatch, 0] - temp.at[imatch, 2]
                    new_rowm = [minus, temp.at[imatch, 3]]
                    new_rowm = pd.DataFrame(new_rowm).transpose()
                    
                    temp = pd.concat([temp, new_rowp])
                    temp = pd.concat([temp, new_rowm])
                    temp = temp.reset_index().drop('index', axis=1)  
                    temp = temp.drop(temp.index[imatch], axis=0)
                    temp = temp.reset_index().drop('index', axis=1)  
            # ((conversion to kelvin))
            for imatch in range(len(temp)):
                for jgroup in range(len(temp.columns)):
                    ele = temp.at[imatch, jgroup]
                    if jgroup < len(temp.columns)-1:
                        next_ele = temp.at[imatch, jgroup+1]
                    if isfloat(ele) and np.isfinite(ele):
                        if isfloat(next_ele):
                            unit = temp.at[imatch, jgroup+2]
                        if isinstance(next_ele, str):
                            unit = next_ele
                        if unit == '°C':
                            temp.at[imatch, jgroup] = t2t.Celsius.to_kelvin(ele)
                        if unit == 'F':
                            temp.at[imatch, jgroup] = t2t.Fahrenheit.to_kelvin(ele)
                    if isinstance(ele, str):
                        temp.at[imatch, jgroup] = np.nan
        # find min max
        min_temp = temp.min().min()
        max_temp = temp.max().max()
        # put min max temp for a single article in a dataframe
        temp_range1 = [min_temp, max_temp]
        temp_range1 = pd.DataFrame(temp_range1, index=('min', 'max')).transpose()
        # put min max temp for each article in a dataframe
        temp_range = temp_range.append(temp_range1)

