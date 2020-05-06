#!/usr/local/bin/python3
# Author: Steve Mullins (steve.mullins@vdot.virginia.gov)
#
# Pull CSV files from Google Sheet and
# Save locally
#

import os
import shutil
from diff_match_patch import diff_match_patch
from gsheets import Sheets
import logging

# logfile
logfile = "gsheets_pull.log"
downloadFolder = ".\\CSV\\"

# Google Sheet Source Information
dashboardID = '1P7WOyJJHyGSLnIzOXOX3hkF2q9VYEuFmze9m9R8eRu4'
sheetsToDownload = ['Provider Splice Points', 'Locations' ]
workbookList = [ 
    ['1P7WOyJJHyGSLnIzOXOX3hkF2q9VYEuFmze9m9R8eRu4', ['Provider Splice Points', 'Locations' ]],
    ['185nu72PQqFK24f5MmUBFC7NO6A5kTLKIe_VACI0Goko', ['Corridors-GIS']],
    ['1AahIsT2b7k_9fHUaztH8J8b7NDGSrgDxawhSK6DPpRg', ['Internet Drops']]
]

# Set up logging
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename=logfile, filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
stderrLogger=logging.StreamHandler()
stderrLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
logging.getLogger().addHandler(stderrLogger)

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        logging.info('Error: Creating directory. ' +  directory)

# Create CSV file folder locally if does not exist
logging.info("Creating CSV folder " + downloadFolder + ".")
createFolder(downloadFolder)

# Authenticate Connection
try:
    # See: https://pypi.org/project/gsheets/
    # Initalize sheet object with authentication
    sheets = Sheets.from_files('~/client_secrets.json', '~/storage.json')
    # Uncomment and run for inital authentication
    # sheets  #doctest: +ELLIPSIS
except OSError:
    logging.info('Error: Could not authenticate.  Check json files in path.')

# Interate through sheet list and download to local CSV files
for workbook in workbookList:
    dashboardID = workbook[0]
    # Create book object for Dashboard Sheet
    dashb = sheets[dashboardID]
    # Get workbook name
    title = dashb.title
    # Download all sheets in list 'sheetsToDownload'
    sheetsToDownload = workbook[1]
    for sheetToDownload in sheetsToDownload:
        csv_file_name = downloadFolder + title + ' - ' + sheetToDownload+'.csv'
        # Copy old downloaded CSV file of sheet
        try:
            shutil.copy(csv_file_name, csv_file_name+'.old')
        except:
            logging.info('Unable to copy file '+csv_file_name)
        # Find sheet in book
        try:
            # Download sheet
            sheet = dashb.find(sheetToDownload)
            logging.info(sheetToDownload + ' downloaded from ' + title)
            # Save sheet to CSV
            sheet.to_csv(csv_file_name, encoding='utf-8', dialect='excel')
            logging.info(csv_file_name + ' saved.')
            
        except:
            logging.info('Unable create file '+csv_file_name)  
        # Create diff and save to log
        try:
            with open(csv_file_name) as csv_new_file:
                csv_new = csv_new_file.read()
            with open(csv_file_name+'.old') as csv_old_file:
                csv_old = csv_old_file.read()
            dmp = diff_match_patch()
            patches = dmp.patch_make(csv_new, csv_old)
            diff = dmp.patch_toText(patches)
            logging.info('##BEGIN DIFF  '+csv_file_name)
            logging.info(diff)
            logging.info('##END DIFF  '+csv_file_name)
        except:
            logging.info('Unable to create diff for '+csv_file_name) 
