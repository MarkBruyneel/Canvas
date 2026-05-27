# Canvas  tool to be able to automatically check Canvas URL's
#
# Author: Mark Bruyneel
#
# Date: 2026-04-30
# Version: 1.0
# Created using Python version 3.10
#
# Re-use note: Make sure to change folder names that are relevant to your computer

import requests
import pandas as pd # version 2.2.3
import time
from loguru import logger #version 0.7.2
from datetime import datetime  # version 5.5

# Show all data in screen
pd.set_option("display.max.columns", None)

# Retry searches section
MAX_RETRIES = 10

# Create year and date variable for filenames etc.
today = datetime.now()
year = today.strftime("%Y")
runday = str(datetime.today().date())

logger.add(f'U:\Werk\OWO\AIP\Canvas_raw_data\Canvas_test_{runday}.log', backtrace=True, diagnose=True, rotation="10 MB", retention="12 months")
@logger.catch()

def main():
    # Step 1: import list of Canvas URLs to check

    # Step 2: Test each link and retrieve status
    # For this step to work you need to log into Canvas in the internet software first (if needed)
    # Provide the file name and location for which to look up data
    excelfile = input('Please provide the location and name of the Excel file.\nExample: C:\\temp\keyword_list.xlsx \n')
    sh_name = input('Please provide the exact sheet name that has the data: \n')
    Canvas_original = pd.read_excel(f'{excelfile}', sheet_name=sh_name, converters={'ISBN': str})

    item = 1
    Size_table1 = Canvas_original.shape[0]
    logger.debug(f'Trying to get Canvas Status for urls starting with nr. {item} until {Size_table1}')
    while item < Size_table1:
        url_test = Canvas_original['url'].loc[Canvas_original.index[item]]
        item_MID = Canvas_original['Material id'].loc[Canvas_original.index[item]]
        try:
            url_len = len(url_test)
            if url_len < 2:
                pass
            else:
                for i in range(MAX_RETRIES):
                    try:
                        response = requests.get(url_test)
                        if response.status_code == 200:
                            logger.debug(f',{item_MID},Still available: {response.status_code},{url_test}')
                            break
                        elif response.status_code == 404:
                            logger.debug(f',{item_MID},Cannot find: {response.status_code},{url_test}')
                            break
                        else:
                            logger.debug(f',{item_MID},Different response: {response.status_code},{url_test}')
                            break
                    except Exception as e:
                        logger.debug(f'Error getting data: {e}. Retrying...')
                        logger.debug(f'Request failed, retrying {i + 1}/{MAX_RETRIES} times...')
                        # Time between retries
                        time.sleep(10)
                time.sleep(2)
        except:
            pass
        item = item + 1
    logger.debug(f'Finished checking Canvas for file availability on {runday}.')
if __name__ == "__main__":
    main()