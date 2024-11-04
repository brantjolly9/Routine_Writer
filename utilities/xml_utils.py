import lxml.etree as et
from pprint import pprint
import logging
import re

logger = logging.getLogger("main.log")

def get_all_rung_strings(l5xPath):
    """
    Function to return a list of tuples container all tags present in the L5X file
    For non-bool tags it returns (value, tagName)
    For bool tags it returns (1, tagName)
    For NOP it returns (0, tagName (NOP()))

    rungs=[
        (value, tagName),
        (1, tagName),
        (0, NOP())
    ]
    
    """
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
