import lxml.etree as et
from pprint import pprint
import logging

logger = logging.getLogger("main.log")

def get_all_rungs(l5xPath):
    try:
        xmlDoc = et.parse(l5xPath)
    except Exception as e:
        print(f"Error reading L5X File at {l5xPath}")
        return none
    root = xmlDoc.getroot()
    RLLcontent = root.findall('Controller/Programs/Program/Routines/Routine/RLLContent/Rung')
    rungList = []
    for rung in RLLcontent[:10]:
        rungText = rung.find("Text").text.strip()
        print(rungText)
        rungList.append(rungText)
    return rungList

def add_cdata(text = str()):
    try:
        text = et.CDATA(text)
    except Exception as e:
        logger.error("ADD CDATA ERROR", exc_info=True)
    return text