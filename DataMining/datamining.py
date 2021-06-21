from bs4 import BeautifulSoup
import codecs
import re
import pandas as pd

# Get article text from a saved html file
path = './ArticlesHtml/4.html'
f = codecs.open(path, 'r', 'utf-8')
document = BeautifulSoup(f.read(),features='html.parser').get_text()
f.close()

# Get RPM
speed_rex = r'(\d+)?,?\s?(\d+)?,?\s?(\d+)?\s?\w+\s(\d+)\srpm'
speed = re.findall(speed_rex, document)

# Keep only a range
# clean tuple list of speed (remove empty string → false min)
speed = [(tuple(int(x) if x.isdigit() else x for x in _ if x)) for _ in speed]
# find minimum speed
min0 = 300000
for match in range(len(speed)):
    if isinstance(speed[match], int):
        min_smatch = speed[match]
    else:
        min_smatch = min(speed[match])
    if min_smatch < min0:
        min0 = min_smatch
        min_speed = min_smatch
# find maximum speed        
max0 = 0
for match in range(len(speed)):
    if isinstance(speed[match], int):
        max_smatch = speed[match]
    else:
        max_smatch = max(speed[match])
    if  max0 < max_smatch:
        max0 = max_smatch
        max_speed = max_smatch
# put min max speed for a single article in a dataframe
speed_range1 = [min_speed, max_speed]
speed_range1 = pd.DataFrame(speed_range1, index=('min', 'max')).transpose()
# put min max speed for each article in a dataframe
speed_range = pd.DataFrame(columns=('min', 'max'))
speed_range = speed_range.append(speed_range1)
