# External Libraries (Dependency recorded with requiremnts.txt)
import lxml.etree as et             # XML library
import logging                      # Logging library (Log functionality is in progress)
import re                           # REGEX library for working with strings
from pprint import pprint           # Pretty Printing (For testing)
import pandas as pd                 # Pandas Library for Excel to Dict Conversion
import os                           # Operating System Library for working with folders
from rung_parser import *
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
        print(f"Rung Number {rungNum} is not valid XML")
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
    allRungs = get_all_rungs(l5xPath)
    print(allRungs[:10])
    parsedRungs = parse_routine(allRungs[:10])
    exl = write_param_sheet(parsedRungs, "dict_testing.csv") 
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

def deconstruct():

    # Refer to directory structure in README.txt
    # workingDir will be located in the root directory, then the *_Files directories will be located in the working dir
    # leave testRootDir as is for this to work (will be changed later)
    rootDir = os.getcwd()

    # Preparing working dir and testing for relevant files
    exeDirPath = os.path.dirname(os.path.realpath(__file__))

    userPath = get_path_from_user(exeDirPath, defaultPath=rootDir, defaultFolder="exeTesting")
    userFolder = os.path.basename(userPath)
    exportedFilesFolder = "Exported_Files"
    resultFilesFolder = "Result_Files"


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
    #dataframe = open_excel_as_pd(excelPath)
    combo(l5xFiles[0])

def make_buffer_dict(coordinates, bufferDict=dict()):
    position = coordinates.split(",")
    rungNum = position[0]
    branch = position[1]
    level = position[2]
    buffers = 0

def ThreeD(a, b, c):
    lst = [[ ['#' for col in range(a)] for col in range(b)] for row in range(c)]
    return lst

def clean_positions(postion):
    pos = postion.split(",")
    clean = []
    try:
        for p in pos:
            clean.append(int(p))
        return clean
    except:
        return [100, 100, 100]

def reconstruct(csvLines):
    curBranch = 0
    curLevel = 0
    buffer = ""
    arr = ThreeD(4, 3, 2)
    bufferArray = arr
    #bufferDict = {{}, {}, {}}
    for line in csvLines[2:]:
        try:
            numItems = len(line)
            pos = clean_positions(line[0])
            command = line[1]
            params = line[2:]
            commandBuffer = command + "(" +  "".join(params) + ")"
            #bufferDict[f"rung{pos[0]}"][f"branch{pos[1]}"][f"level{pos[2]}"] = commandBuffer 
            #print(bufferDict)
            bufferArray[pos[0]][pos[1]][pos[2]] = commandBuffer


        except IndexError as ie:
            print("LIST OUT OF RANGE")
            print(ie)
            print(pos)
        pprint(bufferArray)

def zip(csvLines):
    oldRung = 100
    oldBranch = 100
    oldLevel = 100
    buffers = []
    for line in csvLines:
        print(line)
        pos = clean_positions(line[0])
        mainBuffer = ""
        while pos[0] < oldRung:
            print("RUNG")
            while pos[1] < oldBranch:
                print("BRANCH")
                mainBuffer += "!!"
                while pos[2] <= oldLevel:
                    for b in line[1:]:
                        mainBuffer += "(" + b
                    oldLevel = pos[2]
                    print(pos)
                    print(oldLevel)
                mainBuffer += "??"
                oldBranch = pos[1]
            oldRung = pos[0]
        buffers.append(mainBuffer)
    return buffers

def reeeeee():
    l = [
        [1, 2, 3, 3, 5, 2, 1, 4],
        [9, 8, 4, 2, 4, 6, 7, 8],
        [5, 6, 2, 1, 5, 6, 7, 8]]
    oldPos = 100
    for col in l:
        print(col)
        pos = col[1]
        while oldPos <= pos:
            print("Less Than")
            oldPos = pos

if __name__ == "__main__":
    logger = logging.getLogger("main.log")
    #deconstruct()
    #combo("24-071-Configuration_Routine_RLL.L5X")

    testStr = [("[XIC(SLS1.Sorter.LostBearingFault)[XIO(Hmi.Sorter[0].Faults.MissingBearingFault)ADD(Hmi.Sorter[0].Stats.MissingBearingFaultCount,1,Hmi.Sorter[0].Stats.MissingBearingFaultCount)ADD(Hmi.Sorter[0].Stats.TotalFaultCount,1,Hmi.Sorter[0].Stats.TotalFaultCount),OTE(Hmi.Sorter[0].Faults.MissingBearingFault),XIC(OneSecondPulse)ADD(Hmi.Sorter[0].Stats.MissingBearingCurrentTime,1,Hmi.Sorter[0].Stats.MissingBearingCurrentTime)ADD(Hmi.Sorter[0].Stats.MissingBearingTotalTime,1,Hmi.Sorter[0].Stats.MissingBearingTotalTime)],XIO(SLS1.Sorter.LostBearingFault)CLR(Hmi.Sorter[0].Stats.MissingBearingCurrentTime)];", "COMMENT")]

    parsedRungs = parse_routine(testStr)
    filename = "rung_testing.csv"
    #fullFile = "csv_testing.csv"
    singleLineTest = "single_line.csv"
    write_param_sheet(parsedRungs, singleLineTest)

#    lines = read_param_sheet(filename)
#    buff = zip(lines)
#    print(buff)
#    print("END")
