# External Libraries (Dependency recorded with requiremnts.txt)
import lxml.etree as et             # XML library
import logging                      # Logging library (Log functionality is in progress)
import re                           # REGEX library for working with strings
from pprint import pprint           # Pretty Printing (For testing)
import pandas as pd                 # Pandas Library for Excel to Dict Conversion
import os                           # Operating System Library for working with folders
from rung_parser import parse_routine
# Try to import custom Libraries stored in .\Utilities
# Print an error if not found
try:
    #from createLogger import makeLogger
    from utilities.excel_utils import *
    from utilities.os_utils import *
    from utilities.xml_utils import *
    from utilities import makeLogger

except ModuleNotFoundError as mnf:
    print("Custom Modules Not Found")

def fill_rung_template(root, rungNum, text, comment=None):

    # Convert int to str
    rungNum = str(rungNum)

    # Get the RLLContent container tag to append rung tags to
    RLLContent = root.findall('Controller/Programs/Program/Routines/Routine/RLLContent')

    # Create an XML element from a blank Rung element
    template = et.fromstring(
        '<Rung Number="" Type="N">'
            '\n<Comment></Comment>'
            '\n<Text></Text>\n.'
        '</Rung>')
    oldRung = RLLContent.xpath(f"//Rung[contains(@Number, {rungNum})]")
    oldComment = oldRung.find("Comment").text
    print(oldComment)
    # Check if rungnum is a digit, and fill Rung Number in element  
    if re.search(r"^\d+$", rungNum):
        template.set("Number", rungNum)
    else:
        logger.critical(f"Rung Number: {rungNum} is not an integer")

    # Check for comment, else leave tag blank
    if comment:
        template.find("Comment").text = add_cdata(comment)

    # Fill Rung Element Text Tag with rung text, if the element is valid
    template.find("Text").text = add_cdata(text)
    if isinstance(template, et._Element):
        RLLContent.append(template)
    else:
        logging.warning(f"Number {rungNum} is not valid XML")

    # Return the Filled Template
    return template

def attach_rungs(dataframe):
    for fileName, rungs in dataframe.items():
        fullFileName = f"{fileName}_Routing_RLL.L5X"
        indivXmlFile = et.parse(fullFileName)
        root = indivXmlFile.getroot()
        for rungNum, rung in enumerate(rungs):
            filledTemplate = fill_rung_template(root, rungNum, rung)

def combo(l5xPath):
    allRungs = get_all_rung_strings(l5xPath)
    parsedRungs = parse_routine(allRungs)
    exl = write_param_sheet(parsedRungs, "csv_testing.csv") 
    print("RAN")





def main():
    # Refer to directory structure in README.txt
    # workingDir will be located in the root directory, then the *_Files directories will be located in the working dir
    # leave testRootDir as is for this to work (will be changed later)
    rootDir = os.getcwd()

    userPath = get_path_from_user(defaultPath=rootDir, defaultFolder="exeTesting")
    userFolder = os.path.basename(userPath)
    exportedFilesFolder = "Exported_Files"
    resultFilesFolder = "Result_Files"

    # Preparing working dir and testing for relevant files
    exeDirPath = os.path.dirname(os.path.realpath(__file__))

    # Returns a Dictionary of verified paths
    verifiedPaths = prepare_working_dir(workingDir=userPath)

    # Get relevant path from the dictionary of verified paths
    workingDir = verifiedPaths[userFolder]
    makeLogFile(workingDir)
    excelPath, l5xFiles = check_working_files(workingDir, logger)
    exportedFilesPath = verifiedPaths[exportedFilesFolder] 
    resultFilesPath = verifiedPaths[resultFilesFolder]

    print("\nThe Program has created or verified the following paths:")
    for path in verifiedPaths.values():
        print(path)
    print("File Operations Completed\n--------------------\n")
    # Create the dicionary object (dataframe) from the excel sheet
    dataframe = open_excel_as_pd(excelPath)

    # load an xml file for each routine then fill xml doc with filename's rungs 
    try:
        for fileName, rungs in dataframe.items():

            fullFileName = f"{fileName}_Routine_RLL.L5X"
            fullResultPath = os.path.join(resultFilesPath, fullFileName)
            fullExportedFilePath = os.path.join(exportedFilesPath, fullFileName)
            if fullFileName in l5xFiles:
                print(f"Currently Editing: {fullFileName}")
                indivXmlFile = et.parse(fullExportedFilePath)
                root = indivXmlFile.getroot()

                for rungNum, rung in enumerate(rungs):
                    filledTemplate = fill_rung_template(root, rungNum, rung)
                    print(f"Filled {rungNum} rungs")

                fileWritten = write_to_file(indivXmlFile, fullResultPath)
                print(f"Wrote to: {fullResultPath}\n")
    except AttributeError as ae:
        logger.error("Unable to find dataframe", exc_info=True)

if __name__ == "__main__":
    logger = logging.getLogger("main.log")
    combo("24-071-Configuration_Routine_RLL.L5X")
