## CSV Download for AGOL
Automate downloading of CSV's from Google Sheets.

### Summary
It is very useful to display Google Sheets location data in AGOL with pop-up info.  AGOL has a tool to dynamically link services to Google Sheets, however in some situations direct linking is not possible.  A solution is to download sheets as CSV's and upload as a AGOL services.  This script provides partial automation of the process by downloading predefined sheets as CSV's into a directory.

### Depends
Install dependancies with:
```bash
pip install gsheets 
```
Please follow the directions at https://pypi.org/project/gsheets/ to set up token authentication.

### Directions
The object **workbookList** in file **gsheets_pull.py** contains all the information needed to identify the sheets to be downloaded.

As an example, the following is a **workbookList** object for sheets named **vehicles** and **speed** belonging to a Google Sheets workbook at URL **https://docs.google.com/spreadsheets/d/1P7WOyJJHyGSLnIzOXOX3hkF2q9VYEuFmze9m9R8eRu4/edit?ts=5e0a5c8e#gid=1664742972**
  
```python
workbookList = [
    ['1P7WOyJJHyGSLnIzOXOX3hkF2q9VYEuFmze9m9R8eRu4', ['vehicles', 'speed' ]]
]
```
Multiple Workbooks and sheets can be defined as well:
```python
workbookList = [
    ['1P7WOyJJHyGSLnIzOXOX3hkF2q9VYEuFmze9m9R8eRu4', ['Provider Splice Points', 'Locations' ]],
    ['185nu72PQqFK24f5MmUBFC7NO6A5kTLKIe_VACI0Goko', ['Corridors-GIS']],
    ['1AahIsT2b7k_9fHUaztH8J8b7NDGSrgDxawhSK6DPpRg', ['Internet Drops']]
]
```    

Run for the first time with line
```python
# sheets  #doctest: +ELLIPSIS
```
uncommented to set up an authentication token.  The *depends* section above contains more information.

Run the script and the CSV's will be created in a CSV subfolder along with a log file.
