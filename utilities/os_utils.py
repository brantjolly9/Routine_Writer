import os
import logging
import re
#from utilities import logger
logger = logging.getLogger("main.log")

# Tests for existence of the dir to store the excel and L5X files
# If workinfDir does not exist, make it, then return the verified workingDir path
def prepare_working_dir(
        rootDir = "C:\\",
        workingDir = "testing",
        exportedFilesFolder="Exported_Files",
        resultFilesFolder="Result_Files"
        ):

    #startDir = os.getcwd()
    #os.chdir(rootDir)

    unverifiedPaths = [
        os.path.join(rootDir, workingDir),
        os.path.join(rootDir, workingDir, exportedFilesFolder),
        os.path.join(rootDir, workingDir, resultFilesFolder)
    ]

    verifiedPaths = {}

    # If a path is found or made it gets moved from unverified paths to verified paths
    # Both lists are returned for reference
    for index, path in enumerate(unverifiedPaths):
        try:
            baseName = os.path.basename(path)
            if os.path.isdir(path):
                logger.debug(f"{path} Exists")
                #print(f"{path} Exists")
                pass
            else:
                os.mkdir(path)
                logger.debug(f"{path} Made")
                #print(f"{path} made")
            verifiedPaths[baseName] = path
        except Exception as e: 
            print(f"Error verifying {path}")
            #logger.error(f"Could not verify {path}", exc_info=True)
    #os.chdir(startDir)
    return verifiedPaths
def get_path_from_user(exeDirPath, defaultPath="C:\\", defaultFolder="C:\\exeTesting"):

    print(
        "Make a folder somewhere on the computer (ideally C:\\FolderName)\n"
        "When prompted enter the full path of a folder which contains the ExcelFile.xlsx, Exported_Files, and Result_Files\n"
        "Make sure the folder name only uses letters and underscores i.e. my_folder\n"
        "The full file path should resemble C:\\...\\...\\my_folder\n"
        "A relative file will instruct the program to create a folder in the current one\n"
        )

    workingDir = ""
    print(f"Your Current Directory:\n{exeDirPath}\n")
    while not os.path.isdir(workingDir):
        workingDir = input(f"Enter full or relative file path (defaults to {defaultPath}\\{defaultFolder}): ")
        if workingDir == "":
            workingDir = os.path.join(defaultPath, defaultFolder)
        else:
            workingDir = os.path.join(defaultPath, workingDir)
        try:
            os.mkdir(workingDir)
            print(f"Made Directory at {workingDir}")
        except FileExistsError as fe:
            print(f"Directory exists at {workingDir}")

    return workingDir


def check_working_files(workingDir, logger):
    # workingDir is assumed to be the direcotry containing the xl and l5x files

    # Get cwd and init xl & l5x files
    startDir = os.getcwd()
    exportedFilesPath = os.path.join(workingDir, "Exported_Files")
    excelFilePath = None
    l5xFilePaths = []

    # change to the directory containing the excel file, list all files in workingDir
    # test for presence of excel file, record it
    # if any part of this fails, *FilePath remains None
    try:
        os.chdir(workingDir)
        filesInPath = os.listdir(workingDir)
        for fileName in filesInPath:
            if fileName.endswith(".xlsx"):
                excelFilePath = os.path.abspath(fileName)
        os.chdir(startDir)
    except Exception as e:
        print("Error finding files")
        print(e)

    try:
        os.chdir(exportedFilesPath)
        filesInPath = os.listdir(exportedFilesPath)
        for fileName in filesInPath:
            if fileName.endswith(".L5X"):
                l5xFilePaths.append(fileName)
        os.chdir(startDir)
    except Exception as e:
        print("Error finding Exported_Files")
        print(e)

    if not excelFilePath:
        logger.critical("No Excel File")
        print("No Excel File Found")
    else:
        print(f"Found Excel File: {excelFilePath}")

    if len(l5xFilePaths) == 0:
        logger.critical("No L5X File")
        print("No L5X File Found")
    else:
        print(f"Found {len(l5xFilePaths)} L5X Files")

    return excelFilePath, l5xFilePaths

def makeLogFile(workingDir, logName="main.log"):
    logPath = os.path.join(workingDir, logName)
    try:
        log = open(logPath, "x")
    except FileExistsError as fe:
        log = open(logPath, "a")
    finally:
        log.close()


def user_file_selection(l5xFiles):

    userFiles = []
    testStrings = [
            "1-4",
            "5-1",
            "5",
            "4,5,6",
            "a",
            "1,2,3,4,5,6,7,8,9,10,11",

            ]
    print("Select an L5X File to Get Data From\n(X-Y) for a range\n(X,Y,Z) for individual files")
    for index, lFile in enumerate(l5xFiles):
        print(f"{lFile}: ({index + 1})")
    fileSelection = []
    seperator = None
    validStr = False
    lenOnes = len(l5xFiles) % 10
    lenTens = len(l5xFiles) % 100 // 10

    while not validStr:
        try:
            userInput = input("Selection: ")
            #result = re.search(f"([0-{lenTens}]?[0-{lenOnes}](-|,)?)+", userInput)
            result = re.search(f"(\d(-|,)?)+", userInput)
            #result = re.findall("(\d(-|,)?)+")
            if result != None:
                seperator = result.groups()[-1]
                print(seperator)
                if seperator:
                    for i in result.string.split(seperator):
                        fileSelection.append(int(i) - 1)
                else:
                    fileSelection.append(int(result.string) - 1)
                validStr = True
        except ValueError as ve:
            print(f"Please Enter a Selection in the Range of 0-{len(l5xFiles)}")

    print(fileSelection)
    if seperator == ",":
        for i in fileSelection:
            userFiles.append(l5xFiles[i])
    elif seperator == "-":
        userFiles = l5xFiles[fileSelection[0]:fileSelection[1]+1]
    else:
        userFiles.append(l5xFiles[fileSelection[0]])
    return userFiles
