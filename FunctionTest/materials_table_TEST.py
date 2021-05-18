# -*- coding: utf-8 -*-
"""
Created on Tue May 18 09:06:23 2021

@author: valer
"""

import pandas as pd

ad = {'A': ['wow un pissenlit', 'choucroute', 'bird oiseau', 'choucroute qui sent fort', 'choucroute de pissenlit'], 'B': ['nan', 1, 1, 'nan', 1]}
adf = pd.DataFrame(ad)
adfm = adf[adf.B != 'nan']

bdf = pd.read_csv("CleanWordsOccurence_modified.csv", sep=",")
bdf = bdf.fillna('nan')
bdfm = bdf[bdf.materials != 'nan']