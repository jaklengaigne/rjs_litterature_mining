import os
from bs4 import BeautifulSoup
import codecs
import re
import pandas as pd
import numpy as np

# Iterated throught a bunch of local html file
directory = './ArticlesHtml'
dia_range = pd.DataFrame(columns=('min', 'max'))
for filename in os.listdir(directory):
    if filename.endswith('.html'):
        # Get article text from a saved html file
        path = os.path.join(directory, filename)
        f = codecs.open(path, 'r', 'utf-8')
        document = BeautifulSoup(f.read(),features='html.parser').get_text()
        f.close()
        
        # Get diameter
        dia_rex = r'fib.*\s(\d+\s?±\s?\d+\s?[μ|n]m)|n?a?n?o?fibers?\swith\san?\s?a?v?e?r?a?g?e?\sdiameters?\s.*[\s≈~](\d+?\.?\d+[\s| ]?[μ|n]m)|diameters?\sof\sn?a?n?o?fibers?\s.*\s(\d+?\.?\d+[\s| ]?[μ|n]m)|fibers?\sdiameters?.*\s(\d+?\.?\d+\s?[μ|n]?m?\s\w+\s\d+?\.?\d+\s?[μ|n]m)|fibers?\sdiameters?.*[\s(](\d+[–|-]\d+\s?[μ|n]m)'
        dia = re.findall(dia_rex, document)
        
        # Keep only a range
        # clean tuple list of dia 
        # (remove empty string → false min, space, comma and untis → conversion)
        dia = [(re.split(' and | to |–|-| | | ', x) if isinstance(x, str) else x for x in _ if x) for _ in dia]
        # ((remove generator because it's painfull to work with as beginner in python))
        dia = pd.DataFrame(dia)
        dia = pd.DataFrame(dia[0].tolist())
        # ((change object type because everything is not suppose to be str))
        def isfloat(value):
          try:
            float(value)
            return True
          except ValueError:
            return False
        for i, row in dia.iterrows():
            for j in range(len(row)):
                if isinstance(row[j], str):
                    if row[j].isdigit() or isfloat(row[j]):
                        row[j] = float(row[j])
                if not row[j]:
                    row[j] = np.nan
        # ((special case : ±))
        bool_df = (dia == '±').any(axis=1)         
        for imatch in range(len(dia)):
            if bool_df[imatch]:
                plus = dia.at[imatch, 0] + dia.at[imatch, 2]
                new_rowp = [plus, dia.at[imatch, 3]]
                new_rowp = pd.DataFrame(new_rowp).transpose()
                
                minus = dia.at[imatch, 0] - dia.at[imatch, 2]
                new_rowm = [minus, dia.at[imatch, 3]]
                new_rowm = pd.DataFrame(new_rowm).transpose()
                
                dia = pd.concat([dia, new_rowp])
                dia = pd.concat([dia, new_rowm])
                dia = dia.reset_index().drop('index', axis=1)  
                dia = dia.drop(dia.index[imatch], axis=0)
                dia = dia.reset_index().drop('index', axis=1)  
        # ((conversion to meter))
        for imatch in range(len(dia)):
            for jgroup in range(len(dia.columns)):
                ele = dia.at[imatch, jgroup]
                if jgroup < len(dia.columns)-1:
                    next_ele = dia.at[imatch, jgroup+1]
                if isfloat(ele) and np.isfinite(ele):
                    if isfloat(next_ele):
                        unit = dia.at[imatch, jgroup+2]
                    if isinstance(next_ele, str):
                        unit = next_ele
                    if unit == 'μm':
                        dia.at[imatch, jgroup] = ele*10**-6
                    if unit == 'nm':
                        dia.at[imatch, jgroup] = ele*10**-9
                if isinstance(ele, str):
                    dia.at[imatch, jgroup] = np.nan
        # find min max
        min_dia = dia.min().min()
        max_dia = dia.max().max()
        # put min max dia for a single article in a dataframe
        dia_range1 = [min_dia, max_dia]
        dia_range1 = pd.DataFrame(dia_range1, index=('min', 'max')).transpose()
        # put min max dia for each article in a dataframe
        dia_range = dia_range.append(dia_range1)

