import re
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
    print(f"Ones: {lenOnes}\nTens: {lenTens}")

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
