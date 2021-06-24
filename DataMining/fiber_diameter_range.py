import os
from bs4 import BeautifulSoup
import codecs
import re
import pandas as pd
import numpy as np

# =============================================================================
# # Iterated throught a bunch of local html file
# directory = './ArticlesHtml'
# dia_range = pd.DataFrame(columns=('min', 'max'))
# for filename in os.listdir(directory):
#     if filename.endswith('.html'):
# =============================================================================
dia_range = pd.DataFrame(columns=('min', 'max'))
# Get article text from a saved html file
path = './ArticlesHtml/024.html'
f = codecs.open(path, 'r', 'utf-8')
document = BeautifulSoup(f.read(),features='html.parser').get_text()
f.close()

# Get diameter
dia_rex = r'n?a?n?o?fibers?\swith\san?\s?a?v?e?r?a?g?e?\sdiameters?\s.*[\s≈~](\d+?\.?\d+[\s| ]?[μ|n]m)|diameters?\sof\sn?a?n?o?fibers?\s.*\s(\d+?\.?\d+[\s| ]?[μ|n]m)|fibers?\sdiameters?.*\s(\d+?\.?\d+\s?[μ|n]?m?\s\w+\s\d+?\.?\d+\s?[μ|n]?m?)|fibers?\sdiameters?.*[\s(](\d+[–|-]\d+\s?[μ|n]m)'

test1 = 'polypropylene (PP) nanofibers with an average diameter of 790 nm are successfully prepared'
test2 = 'Fang et al.11 prepared tin fluorophosphate glass fibers with average diameters ranging from 2 to 4 μm via centrifugal forcespinning.'
test3 = 'the diameter of the centrifugal differential disk is 200 mm, and'
test4 = 'the fibers were twisted into a cylinder about 3 mm in diameter and 20 mm in length, clamped on the nanotensile testing system (Aglient T150 UTM), the load value at start was 750 μN and'
test5 = 'Table 2.The Influence of Four Studied Factors on the Average Diameter of Fibers Experimental number A B C D Average diameter (μm) 1 1 1 1 1 6.91'
test6 = 'This is because the average diameter of fibers in Group 7 (0.79 μm) is much smaller than that in Group 2 (7.44 μm)'
test7 = 'The maximum average diameter of fibers was 8.09 μm, '
test8 = 'diameter of nanofibers was 160 nm for Group 7, as it is shown in Figure 7. It could indicate that the MDCE could fabricate the nanosized ultrafine fibers with a diameter of ~100 nm'
dia = re.findall(dia_rex, document)
dia1 = re.findall(dia_rex, test1)
dia2 = re.findall(dia_rex, test2)
dia3 = re.findall(dia_rex, test3)
dia4 = re.findall(dia_rex, test4)
dia5 = re.findall(dia_rex, test5)
dia6 = re.findall(dia_rex, test6)
dia7 = re.findall(dia_rex, test7)
dia8 = re.findall(dia_rex, test8)
# =============================================================================
# # Keep only a range
# # clean tuple list of dia 
# # (remove empty string → false min, space, comma and untis → conversion)
# dia = [(x.replace(',', '').replace(' ', '') if isinstance(x, str) else x for x in _ if x) for _ in dia]
# dia = [(tuple(int(x) if x.isdigit() else x for x in _ if x)) for _ in dia]
# # find minimum dia
# min0 = 300000000
# for match in range(len(dia)):
#     if isinstance(dia[match], int):
#         min_dmatch = dia[match]
#     else:
#         min_dmatch = min(dia[match])
#     if min_dmatch < min0:
#         min0 = min_dmatch
#         min_dia = min_dmatch
# # find maximum dia        
# max0 = 0
# for match in range(len(dia)):
#     if isinstance(dia[match], int):
#         max_dmatch = dia[match]
#     else:
#         max_dmatch = max(dia[match])
#     if  max0 < max_dmatch:
#         max0 = max_dmatch
#         max_dia = max_dmatch
# # if no match is found
# if not dia:
#     min_dia = np.nan
#     max_dia = np.nan
#     min_dmatch = None
#     max_dmatch = None
# # put min max dia for a single article in a dataframe
# dia_range1 = [min_dia, max_dia]
# dia_range1 = pd.DataFrame(dia_range1, index=('min', 'max')).transpose()
# # put min max dia for each article in a dataframe
# dia_range = dia_range.append(dia_range1)
# # clean before the new iteration of the loop
# del min_dmatch, min_dia, max_dmatch, max_dia
# =============================================================================
