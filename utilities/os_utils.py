import os
import logging
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
def get_path_from_user(defaultPath="C:\\", defaultFolder="C:\\exeTesting"):

    print(
        "Make a folder somewhere on the computer (ideally C:\\FolderName)\n"
        "When prompted enter the full path of a folder which contains the ExcelFile.xlsx, Exported_Files, and Result_Files\n"
        "Make sure the folder name only uses letters and underscores i.e. my_folder\n"
        "The full file path should resemble C:\\...\\...\\my_folder\n"
        "A relative file will instruct the program to create a folder in the current one\n"
        )
    
    workingDir = ""
    exeDirPath = os.path.dirname(os.path.realpath(__file__))
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