import lxml.etree as et
from pprint import pprint

l5xPath = "HmiSorter_Routine_RLL.L5X"
def get_all_rungs(l5xPath):
    xmlDoc = et.parse(l5xPath)
    root = xmlDoc.getroot()
    RLLcontent = root.findall('Controller/Programs/Program/Routines/Routine/RLLContent/Rung')
    rungList = []
    for rung in RLLcontent[:10]:
        rungText = rung.find("Text").text.strip()
        print(rungText)
        rungList.append(rungText)
    return rungList

rl = get_all_rungs(l5xPath)