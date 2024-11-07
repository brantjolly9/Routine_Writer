"""
Holds the excel utilities for the main PLC routine config program
"""
import openpyxl
import pandas as pd
import numpy as np
import logging
import json
import logging
import csv
#from utilities import logger
logger = logging.getLogger("main.py")

# Open the Excel doc at the given path and returns the relevant sheet,
# sheet default is "RawData"
def open_excel(excelPath, sheetName="RawData"):
    # Simpply opens excel and returns the passed in sheet name (defaults to "RawData")

    try:
        wb = openpyxl.load_workbook(excelPath)
        sheet = wb[sheetName]
        return sheet
    except Exception as e:
        logger.error(f"Cant open excel sheet at {excelPath}", exc_info=True)
        return None
def open_excel_as_pd(excelPath, sheetName="RawData"):
    """
    THIS IS THE ONLY FUNCTION USED, IGNORE OTHERS FOR NOW
    Convert the excel sheet (at "sheetName" of "excelPath") to a python dictionary and replace NaN with None (Conversion between different formats of the same thing)
    Write the Dictionary to the file sheet.json
    except statements are general error handling
    """
    toReturn = {}
    try:
        sheet = pd.read_excel(excelPath, sheet_name=sheetName)
        sheet.replace(np.nan, None, inplace=True)
        data = sheet.to_dict('list')
        with open("sheet.json", "w") as jsonFile:
            json.dump(data, jsonFile, ensure_ascii=True, indent=4)
        logger.debug(f"Excel DataFram Shape: {sheet.shape}")
        toReturn = data
    except FileNotFoundError as fnf:
        logger.error(f"Cant open sheet at path: {excelPath}")
        toReturn = None
    except TypeError as te:
        logger.error("Type Error during DataFrame creation", exc_info=True)
    except Exception as e:
        logger.debug(e.args)
        logger.error("General Error creating dataframe", exc_info=True)
        toReturn = None
    finally:
        return toReturn

def read_column(sheet, column):

    # Read column from passed sheet, column defaults to 2, but each column should have a different routine
    rungNum = 0
    rungsText = []
    rungText = ""
    while rungText != None:

        # excel row number is rung number + 1 
        try:
            rungText = sheet.cell(row=rungNum + 1, column=column).value
        except Exception as e:
            logging.error(f"Cant real cell at row: {rungNum + 1}, col: {column}")
        rungsText.append(rungText)
        rungNum += 1  

    # Remove last rung (none)
    rungsText.remove(None)
    return rungsText

def get_column_titles(sheet):
    # Returns list of column titles from _sheet_
    columnTitles = []
    data = {}
    rows = sheet["1"]

    for columnTitle in rows:
        columnTitles.append(columnTitle.value)
    return columnTitles

def write_param_sheet(routine, filename):
    header = ["Rung", "Function", "Arguments"]
    new_rung = [""]

    formatted_routine = []
    for rung in routine:
        for function in rung:
            line_holder = []
            position = f"{function[0][0]}-{function[0][1]}-{function[0][2]}"
            line_holder.append(position)

            for item in function[1]:
                line_holder.append(item)
        
            formatted_routine.append(line_holder)
        formatted_routine.append(new_rung)

    for i in formatted_routine:
        print(i)

    # Writing to CSV using csv.writer
    #Create Exception if write permission is denied for file being open in another location
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        
        writer.writerows(formatted_routine)
