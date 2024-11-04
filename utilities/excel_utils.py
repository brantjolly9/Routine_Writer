"""
Holds the excel utilities for the main PLC routine config program
"""
import openpyxl
import pandas as pd
import numpy as np
import logging
import json
import logging
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
