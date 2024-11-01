import lxml.etree as et
from pprint import pprint
import logging

logger = logging.getLogger("main.log")

def get_all_rung_strings(l5xPath):
    try:
        xmlDoc = et.parse(l5xPath)
    except Exception as e:
        print(f"Error reading L5X File at {l5xPath}")
        return None

    root = xmlDoc.getroot()
    RLLcontent = root.findall('Controller/Programs/Program/Routines/Routine/RLLContent/Rung')
    rungList = []
    for rung in RLLcontent[:10]:
        rungText = rung.find("Text").text.strip()
        print(rungText)
        rungList.append(rungText)
    return rungList

def add_cdata(text = str()):
    # add CDATA prefix & suffix to element text; required to use special characters in L5X document
    # <Tag> SOME TEXT </Tag> --> <Tag> <![CDATA[ SOME TEXT ]]> </Tag>

    try:
        text = et.CDATA(text)
    except Exception as e:
        logger.error("ADD CDATA ERROR", exc_info=True)
    return text

def write_to_file(xmlFile, resultPath):
    # arg 2-4 populate xml declaration
    # <?xml version='1.0' encoding='UTF-8' standalone='yes'?>
    try:
        xmlFile.write(
            resultPath,
            xml_declaration=True,
            encoding="UTF-8",
            standalone=True)
        return True
    except Exception as e:
        logger.error(f"Cant write to file: {resultPath}", exc_info=True)
        return False
