import lxml.etree as et
from pprint import pprint
import re

l5xPath = "exeTesting\\Exported_Files\\Configuration_Routine_RLL.L5X"
xmlDoc = et.parse(l5xPath)
root = xmlDoc.getroot()
RLLContent = root.findall('Controller/Programs/Program/Routines/Routine/RLLContent/Rung')

rungs = []

for rung in RLLContent[:10]:
    rungText = rung.find("Text").text.strip()
    pairs = re.findall(r"\((.*?)\)", rungText)
    for pair in pairs:
        if "," in pair:
            pair = pair.split(",")
    rungs.append(pair)


pprint(rungs)
