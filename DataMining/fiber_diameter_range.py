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
path = './ArticlesHtml/005.html'
f = codecs.open(path, 'r', 'utf-8')
document = BeautifulSoup(f.read(),features='html.parser').get_text()
f.close()

# Get diameter
dia_rex = r'fibers?\sdiameters?.*\s(\d+?\.?\d+\s?[μ|n]?m?\s\w+\s\d+?\.?\d+\s?[μ|n]?m?)|fibers?\sdiameters?.*[\s(](\d+[–|-]\d+\s?[μ|n]m)'

test1 = '9-11 recent efforts have focused on developing techniques for producing nanofibers with diameters less than 1 μm'
test2 = 'iRJS control over the morphology, diameter, and alignment of sheets. a) Traditional nanofiber spinning systems relying on volatile solvents cause beading as described by the Raleigh–Plateau instability and revealed in SEM images of nylon (left scale bar = 20 μm, right scale bar = 5 μm)'
test3 = 'For the case of nylon fibers, average fiber diameter decreased with increasing air gap distance (2 cm < d < 6 cm) and extruder rotation speed (15 kRPM < ω < 45 kRPM). In contrast, fiber diameter increased with increasing weight per volume solution concentration (5% w/v < C < 20% w/v). Within this parameter space, average nylon fiber diameters of 250 nm to 2.75 μm were produced (Figure 2c–e, Figure S2, Supporting Information).'
test4 = 'Commercial PPTA fiber diameters are on the order of ≈10 μm and possess an inhomogeneous core-skin morphology that depends on proprietary production processes.'
test5 = 'increasing spinning speed from 45 k RPM to 65k RPM decreased nanofiber diameter from 1300 to 800 nm (Figure 4a).'
test6 = 'Spun at 65k RPM, PPTA concentrations of 1, 3, 5, or 10% (wt/v%) produced sheets of nanofibers with mean diameters of ≈500, 800, 850, or 900 nm, respectively (Figure 4a–d).'
test7 = 'While commercial fiber diameters typically range from 10 to 20 μm,56 the significantly smaller diameter of the iRJS PPTA nanofibers (500–1000 nm) provides a 10–20 times increase in surface area-to-volume ratio.'
test8 = 'fiber diameters ranged from 750 to 900 nm, density was .43 gm cm−3, and OOP values were .95 or greater. Mechanical testing of alginate–gelatin nanofibers after transglutaminase crosslinking (Modernist Pantry, Portsmouth, NH) crosslinking was obtained with a biaxial tension test (CellScale BioTester, Waterloo, Canada). For alginate nanofibers tested mechanically, fiber diameters ranged from 600 to 800 nm'
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
