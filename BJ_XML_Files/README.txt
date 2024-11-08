NOTES:
    The .L5X file extension behaves identically to a .XML file
    All logging functionality is still in progress so ignore any reference to loggers, logging, and error messages
    Most functions are defined in the .py scripts located in the "utilities" folder, main.py basically just brings them together
        excel_utils.py handles all excel stuff (only one used function: open_excel_as_pd())
        os_utils.py handles making and checking for folder existence
    You can mostly ignore any file that isnt .py or .txt

This program aims to read a string of text, generated using excel equations, from an excel document that a user fills out.
Whether this ends up as one sheet per routine or one sheet for all exports is undecided and does not greatly alter the program logic.

First the program records its executable path and tests for the existence of a folder containing an excel file and two folders containing the original and result L5X Files.
If that folder and those files are found then the program records their paths. 
For testing, the program is expecting a file structure like the following, but "workingDir" can be placed anywhere
.
└── config_project
    ├── main.py
    ├── utilities
    │   ├── os_utils.py
    │   └── excel_utils.py
    └── workingDir
        ├── excelFile.xlsx
        ├── Exported_Files
        │   ├── Routine1
        │   ├── Routine2
        │   └── Routine3
        └── Result_Files
            ├── Result1
            ├── Result2
            └── Result3


The Excel Path is used to open the Excel file with the following expected layout:

+-----------+-----------+----------+-----+
| Routine 1 | Routine 2 | Routine3 | ... |
+-----------+-----------+----------+-----+
| Rung 1    | Rung 1    | Rung 1   |     |
| Rung 2    | Rung 2    | Rung 2   |     |
| Rung 3    | Rung 3    | Rung 3   |     |
| ...       | ...       | ...      |     |
+-----------+-----------+----------+-----+

This spreadsheet is then converted to a python dictionary with the following shape:
    {
        Routine1Name:
            [
                Rung1,
                Rung2,
                Rung3,
                ...
            ],
        Routine2Name:
            [
                Rung1,
                Rung2,
                Rung3,
                ...
            ],
    }   ...

The number of routines and number of rungs within a routine are arbitrary; the program will scan for the presence of any Excel Cells, instead of a set number of them.
The program then goes through a list of L5X files names generated from the excel sheet (should match the file name in the working directory) and perfoms the following logic on each:
    Fill out the rest of the file name: "fileName" --> "fileName"_Routine_RLL.L5X
    Load the file into the variable "indivXmlFile" then get its "root"
    For each rung in the list of rung text:
        Fill out a defined template with the rung number, rung text, and a comment if one already exists
        Add or overwrite the existing rung at "rungNumber", preserving the comment
Finally the program will write the L5X file stored in "indivXmlFile" to a new L5X file (for testing, final revision will likely overwrite the original file)

