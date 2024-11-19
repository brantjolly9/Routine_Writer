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
    from rung_builder import *

except ModuleNotFoundError as mnf:
    print("Custom Modules Not Found")

# Problem lies here !!!!!!!!!!!!!!!!!!!
def fill_rung_template(root, rungNum, text, comment=None):

    # Convert int to str
    rungNum = str(rungNum)

    # Create an XML element from a blank Rung element
    template = et.fromstring(
        '<Rung Number="" Type="N">'
            '\n<Comment></Comment>'
            '\n<Text></Text>\n.'
        '</Rung>')
    # Check if rungnum is a digit, and fill Rung Number in element  
    if re.search(r"^\d+$", rungNum):
        template.set("Number", rungNum)
    else:
        logger.critical(f"Rung Number: {rungNum} is not an integer")

    # Check for comment, else leave tag blank
    if comment != "":
        template.find("Comment").text = add_cdata(comment.strip())

    # Fill Rung Element Text Tag with rung text, if the element is valid
    template.find("Text").text = add_cdata(text.strip())
    print(et.tostring(template))

    # Return the Filled Template
    return template

def new_attach_rungs(rungList, outputFile, xmlDoc):
    root = xmlDoc.getroot()
    # Get the RLLContent container tag to append rung tags to
    RLLContent = root.findall('Controller/Programs/Program/Routines/Routine/RLLContent')
    for rungNum, rung in enumerate(rungList):
        template = fill_rung_template(root, rungNum, rung[0], rung[1])
        if isinstance(template, et._Element):
            RLLContent.append(template)
        else:
            print(f"Rung Number {rungNum} is not valid XML")
            logging.warning(f"Number {rungNum} is not valid XML")

def unzip(l5xFile):
    csvName = l5xFile.split(".")[0] + ".csv"
    l5xPath = os.path.join(L5X_FILES_PATH, l5xFile)
    csvPath = os.path.join(CSV_FILES_PATH, csvName)
    allRungs = get_all_rungs(l5xPath)
    with open("inputRungs.txt", "w") as ir:
        ir.writelines(allRungs[1])
    parsedRungs = parse_routine(allRungs)
    exl = write_param_sheet(parsedRungs, csvPath) 


def reconstruct(csvFile, outputFile, inputFile):
    # inputFile is opened because lxml.etree needs an open and non-empty file
    # to write to outputFile
    #
    #  formattedRungs = [(rungText, commentText)]

    # *Path is generated from the global *FilesPath var set in main()
    inputPath = os.path.join(CSV_FILES_PATH, inputFile)
    outputPath = os.path.join(L5X_FILES_PATH, outputFile)
    csvPath = os.path.join(CSV_FILES_PATH, csvFile)
    filePaths = {
            'inputPath': os.path.join(CSV_FILES_PATH, inputFile),
            'outputPath': os.path.join(L5X_FILES_PATH, inputFile),
            'csvPath': os.path.join(CSV_FILES_PATH, csvFile),
            }

    #for filePath in filePaths.values():
    #    if not os.path.exists(filePath):
    #        print("FILE" + filePath)
    #        with open(filePath, "w") as fp:
    #            print(f"Created {filePath}")
    try:
        with open(filePaths["outputPath"], "x") as op:
            print("OPENED")
    except FileExistsError as fe:
        print("ALREADY EXISTS")

    #xmlFile = et.parse(filePaths['inputPath'])
    xmlFile = et.parse(inputFile)
    pprint(filePaths)

    # Formatted Rungs returns correct data from csv
    formattedRungs = routine_handler(csvPath)

    new_attach_rungs(formattedRungs, outputPath, xmlFile)
    write_to_file(xmlFile, outputPath)

#    with open("outputRungs.txt", "w") as opr:
#        opr.writelines(formattedRungs[1])

def main():
    # Set global vars to be used in folder and file creation, should work on Windows
    global userWorkingDir
    global L5X_FILES_PATH
    global CSV_FILES_PATH
    l5xFilesFolder = "L5X_Files"
    csvFilesFolder = "CSV_Files"

    # Refer to directory structure in README.txt
    # workingDir will be located in the root directory, then the *_Files directories will be located in the working dir
    # leave testRootDir as is for this to work (will be changed later)
    rootDir = os.getcwd()

    # Preparing working dir and testing for relevant files
    exeDirPath = os.path.dirname(os.path.realpath(__file__))

    userPath = get_path_from_user(exeDirPath,
                                  defaultPath=rootDir,
                                  defaultFolder="csv_Tester")
    userFolder = os.path.basename(userPath)

    # Returns a Dictionary of verified paths
    verifiedPaths = prepare_working_dir(workingDir=userPath)

    # Get relevant path from the dictionary of verified paths
    userWorkingDir = verifiedPaths[userFolder]
    makeLogFile(userWorkingDir)
    csvFiles, l5xFiles = check_working_files(userWorkingDir, logger)
    L5X_FILES_PATH = verifiedPaths[l5xFilesFolder]
    CSV_FILES_PATH = verifiedPaths[csvFilesFolder]
    print("\nThe Program has created or verified the following paths:")
    for path in verifiedPaths.values():
        print(path)
    print("File Operations Completed\n--------------------\n")

    print("(R)econstruct or (D)econstruct?")
    userChoice = None
    while userChoice != "D" and userChoice != "R":
        userChoice = input("Enter Choice: ")

    if userChoice == "R":

        csvFileSelection = user_file_selection(csvFiles)

        # inputFile will eventually become the template. In essence reconstruct() adds all the rungs from the csvFile to the open xmlDoc i.e. inPutFile then writes the result to outputFile
        inputFile = "24-071-Configuration_Routine_RLL.L5X"
        fileName = inputFile.split(".")[0]

        for csvFile in csvFileSelection:
            outputFile = csvFile.replace(".csv", ".L5X")
            reconstruct(csvFile=csvFile,
                        outputFile=outputFile,
                        inputFile="template.L5X")

    elif userChoice == "D":
        l5xFileSelection = user_file_selection(l5xFiles)
        for l5xFile in l5xFileSelection:
            unzip(l5xFile)


if __name__ == "__main__":
    global logger
    logger = logging.getLogger("main.log")
    main()
