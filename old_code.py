
def old_main():
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
