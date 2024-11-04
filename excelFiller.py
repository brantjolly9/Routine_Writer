import lxml.etree as et
from pprint import pprint
import re
from utilities.xml_utils import get_all_rung_strings

def split_rungs(l5xPath):
    rungs = []
    xmlDoc = et.parse(l5xPath)
    root = xmlDoc.getroot()
    RLLContent = root.findall('Controller/Programs/Program/Routines/Routine/RLLContent/Rung')
    for rung in RLLContent:
        rungText = rung.find("Text").text.strip()
        if "NOP" in rungText:
            rungs.append((0, rungText.replace(";", "")))
        else:
            pairs = re.findall(r"\((.*?)\)", rungText)
            for pair in pairs:
                if "," in pair:
                    rungs.append(tuple(pair.split(",")))
                else:
                    rungs.append(("1", pair))
    return rungs

l5xPath = "exeTesting\\Exported_Files\\Configuration_Routine_RLL.L5X"
rungs = get_all_rung_strings(l5xPath)
pprint(rungs)