from bs4 import BeautifulSoup
import codecs
import re

# Get article text from a saved html file
path = './ArticlesHtml/4.html'
f = codecs.open(path, 'r', 'utf-8')
document = BeautifulSoup(f.read(),features='html.parser').get_text()
f.close()

# Get the RPM range
teststr1 = 'rotational speed between 650, 1700 and 2800 rpm'
teststr2 = 'rotational speed greater than 1700 rpm cause the formation'
teststr3 = 'synthesized PLA (at 650 rpm) decreased'
teststr4 = 'Table 3. The average fiber diameters of non-woven PLA fiber (L130).Rotational speed (rpm)Average fiber diameter (μm)190 °C210 °C230 °C65018.6 ± 5.311.8 ± 3.511.2 ± 4.7170015.4 ± 4.513.3 ± 5.711.4 ± 4.7280014.1 ± 5.49.6 ± 4.15.5 ± 2.7PLA, polylactic acid.'
speed1 = re.findall(r'(\d+)?,? ?(\d+)?,? ?(\d+)? ?\w+ (\d+) rpm', teststr1)
speed2 = re.findall(r'(\d+)?,? ?(\d+)?,? ?(\d+)? ?\w+ (\d+) rpm', teststr2)
speed3 = re.findall(r'(\d+)?,? ?(\d+)?,? ?(\d+)? ?\w+ (\d+) rpm', teststr3)
speed4 = re.findall(r'(\d+)?,? ?(\d+)?,? ?(\d+)? ?\w+ (\d+) rpm', teststr4)
speed = re.findall(r'(\d+)?,? ?(\d+)?,? ?(\d+)? ?\w+ (\d+) rpm', document)



