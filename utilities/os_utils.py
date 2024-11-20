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
        exportedFilesFolder="L5X_Files",
        resultFilesFolder="CSV_Files"
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
    return verifiedPaths
def get_path_from_user(exeDirPath, defaultPath="C:\\", defaultFolder="C:\\exeTesting"):

    print(
        "Make a folder somewhere on the computer (ideally C:\\FolderName)\n"
        "When prompted enter the full path of a folder which contains the L5X_Files, and CSV_Files\n"
        "Make sure the folder name only uses letters and underscores, no spaces; i.e. my_folder\n"
        "The full file path should resemble C:\\...\\...\\my_folder\n"
        "A relative file will instruct the program to create a folder in the current one\n"
        "Press \'Enter\' for the default folder\n"
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


def check_working_files(workingDir, logger, csvFolder="CSV_Files", l5xFolder="L5X_Files"):
    # workingDir is assumed to be the direcotry containing the xl and l5x files

    # Get cwd and init xl & l5x files
    startDir = os.getcwd()
    l5xFilesPath = os.path.join(workingDir, l5xFolder)
    csvFilesPath = os.path.join(workingDir, csvFolder)
    excelFilePath = None
    l5xFilePaths = []
    csvFilePaths = []

    # change to the directory containing the excel file, list all files in workingDir
    # test for presence of excel file, record it
    # if any part of this fails, *FilePath remains None
    try:
        os.chdir(csvFilesPath)
        filesInPath = os.listdir(csvFilesPath)
        for fileName in filesInPath:
            if fileName.endswith(".csv"):
                #excelFilePath = os.path.abspath(fileName)
                csvFilePaths.append(fileName)
        os.chdir(startDir)
    except Exception as e:
        print("Error finding files")
        print(e)

    try:
        os.chdir(l5xFilesPath)
        filesInPath = os.listdir(l5xFilesPath)
        for fileName in filesInPath:
            if fileName.endswith(".L5X"):
                l5xFilePaths.append(fileName)
        os.chdir(startDir)
    except Exception as e:
        print("Error finding L5X_Files")
        print(e)

    if len(csvFilePaths) == 0:
        logger.critical("No Excel File")
        print("No Excel File Found")
    else:
        print(f"Found {len(csvFilePaths)} CSV Files")

    if len(l5xFilePaths) == 0:
        logger.critical("No L5X File")
        print("No L5X File Found")
    else:
        print(f"Found {len(l5xFilePaths)} L5X Files")

    return csvFilePaths, l5xFilePaths


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
    fileSelection = []
    seperator = None
    validStr = False
    #lenOnes = len(l5xFiles) % 10
    #lenTens = len(l5xFiles) % 100 // 10

    print("\nSelect an L5X File to Get Data From\n(X-Y) for a range\n(X,Y,Z) for individual files")
    print("-------------------------------------")
    for index, lFile in enumerate(l5xFiles):
        print(f"{lFile}: ({index + 1})")

    while not validStr:
        try:
            userInput = input("Selection: ")
            #result = re.search(f"([0-{lenTens}]?[0-{lenOnes}](-|,)?)+", userInput)
            result = re.search(r"(\d(-|,)?)+", userInput)
            #result = re.findall("(\d(-|,)?)+")
            if result != None:
                seperator = result.groups()[-1]
                if seperator:
                    for i in result.string.split(seperator):
                        fileSelection.append(int(i) - 1)
                else:
                    fileSelection.append(int(result.string) - 1)
                validStr = True
        except ValueError as ve:
            print(f"Please Enter a Selection in the Range of 0-{len(l5xFiles)}")

    # Fill userFiles according to seperator (',' | '-' | '')
    if seperator == ",":
        for i in fileSelection:
            userFiles.append(l5xFiles[i])
    elif seperator == "-":
        userFiles = l5xFiles[fileSelection[0]:fileSelection[1]+1]
    else:
        userFiles.append(l5xFiles[fileSelection[0]])
    return userFiles



