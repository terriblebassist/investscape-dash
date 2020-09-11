# Welcome to Investscape!

An app designed using [dash](https://dash.plotly.com/), which provides a dashboard through which you can track your mutual fund (India) investments.


# Prerequisites

 - Python 3
 - Virtualenv
 - Google Sheet (containing list of transactions in format specified below)

## CSV Format for list of transactions
Refer  ```transaction_format.csv``` . Project references a Google Sheet, but can be modified to reference local csv file.


### Format Description
| date | scheme_code | scheme_name | value | units |
|--|--|--|--|--|
| 01-12-2019 | 118989 | HDFC Mid Cap Opportunities Fund | 20000 | 100

 1. **date** : plain text, format DD/MM/YYYY. (Example: 01/12/2020)
 2. **scheme_code**: integer, MF scheme code as per AMFI website(```https://www.amfiindia.com/spages/NAVAll.txt```)
 3. **scheme_name**: plain text
 4. **value**: float, invested amount (INR)
 5. **units**: float, units allotted


**NOTE**:
> - Use header names exactly as is.

## Setting up Google Sheets

 1. Follow this [link](https://developers.google.com/sheets/api/quickstart/python) to set up your google account. Place the generated ```credentials.json``` in project root directory.
 2. Replace the variable ```SPREADSHEET_ID(app.py:18)``` by the value marked by "xxx...xx" in this sample Google Sheets URL ```https://docs.google.com/spreadsheets/d/xxxxxxxxxxxxxxx/edit```
 3. Replace the variable ```RANGE_NAME(app.py:19)``` by the tab name of the sheet of interest.

# Run the app
#### Checkout the repo and set up Virtualenv
 1. `git clone git@github.com:terriblebassist/investscape-dash.git`
 2. `cd investscape-dash`
 3. `virtualenv venv`
 4. `source venv/bin/activate`
 #### Install dependencies and run app

 5. `pip install -r requirements.txt`
 6. `python app.py`


> **NOTE**: On first run, you will be redirected to Google's login page and asked to permit the usage of Google Sheets API.
