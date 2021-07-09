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
        dia_rex = r'nozzles?\s+diameters?\s+\w+\s+(\d+?\.?\d+\s?[μnm]m)|syringes?\s+diameters?\s+\w+\s+(\d+?\.?\d+\s?[μnm]m)|needles?\s+diameters?\s+\w+\s+(\d+?\.?\d+\s?[μnm]m)|holes?\s+diameters?\s+\w+\s+(\d+?\.?\d+\s?[μnm]m)|orifices?\s+diameters?\s+\w+\s+(\d+?\.?\d+\s?[μnm]m)|(\d+?\.?\d+\s?[μnm]?m?\s\w+\s\d+?\.?\d+\s?[μnm]m)\s+diameters?\s+orifices?|orifices?\s+diameters?\s+.*\s+(\d+?\.?\d+\s?[μnm]?m?\s+.*\s+\d+?\.?\d+\s?[μnm]m)|diameters?\s+.*\s+orifices?\s+\w+\s+(\d+\s?[μnm]m)|diameters?\s+.*\s+orifices?\s+.*\s+(\d+\s?\s+\w+\s+\d+?\.?\d+\s?[μnm]m)'
        dia = re.findall(dia_rex, document)
        
        # Keep only a range
        # clean tuple list of dia 
        # (remove empty string → false min, space, comma and untis → conversion)
        dia = [(re.split('\s+and\s+|\s+to\s+|\s+or\s+|–|-| | | |,\s+and\s+', x) if isinstance(x, str) else x for x in _ if x) for _ in dia]
        # ((remove generator because it's painfull to work with as beginner in python))
        dia = pd.DataFrame(dia)
        if not dia.empty:
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
            difimatch = 0     
            for imatch in range(len(dia)):
                if bool_df[difimatch]:
                    plus = dia.at[difimatch, 0] + dia.at[difimatch, 2]
                    new_rowp = [plus, dia.at[difimatch, 3]]
                    new_rowp = pd.DataFrame(new_rowp).transpose()
                    
                    minus = dia.at[difimatch, 0] - dia.at[difimatch, 2]
                    new_rowm = [minus, dia.at[difimatch, 3]]
                    new_rowm = pd.DataFrame(new_rowm).transpose()
                    
                    dia = pd.concat([dia, new_rowp])
                    dia = pd.concat([dia, new_rowm])
                    dia = dia.reset_index().drop('index', axis=1)  
                    dia = dia.drop(dia.index[difimatch], axis=0)
                    dia = dia.reset_index().drop('index', axis=1)
                    difimatch -= 1
                difimatch += 1 
            # ((conversion to meter))
            for imatch in range(len(dia)):
                for jgroup in range(len(dia.columns)):
                    ele = dia.at[imatch, jgroup]
                    if jgroup < len(dia.columns)-1:
                        next_ele = dia.at[imatch, jgroup+1]
                    if len(dia.columns)>2 and jgroup < len(dia.columns)-2:
                        next_next_ele = dia.at[imatch, jgroup+2]
                    if isfloat(ele) and np.isfinite(ele):
                        if isfloat(next_ele):
                            if 'next_next_ele' in locals() and isfloat(next_next_ele):
                                unit = dia.at[imatch, jgroup+3]
                            else:
                                unit = dia.at[imatch, jgroup+2]
                        if isinstance(next_ele, str):
                            unit = next_ele
                        if unit == 'mm':
                            dia.at[imatch, jgroup] = ele*10**-3
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

