# Welcome to Investscape!

An app designed using [dash](https://dash.plotly.com/), which provides a dashboard through which you can track your mutual fund (India) investments.

# Prerequisites
- Python 3
- Virtualenv
- Google Sheet (containing list of transactions in format specified below)
- Google Sheets API enabled

## CSV Format for list of transactions
Refer ```docs/transaction_format.csv``` .

### Format Description
| date | scheme_code | scheme_name | value | units |
|--|--|--|--|--|
| 01-12-2019 | 118989 | HDFC Mid Cap Opportunities Fund | 20000 | 100

1.  **date** : plain text, format DD/MM/YYYY. (Example: 01/12/2020)
2.  **scheme_code**: integer, MF scheme code as per AMFI website(```https://www.amfiindia.com/spages/NAVAll.txt```)
3.  **scheme_name**: plain text
4.  **value**: float, invested amount (INR)
5.  **units**: float, units allotted

**NOTE**:
>  - Use header names exactly as is.

## Setting up Google Sheets
**If running on a server, follow below steps:**
1. Follow this [link](https://console.cloud.google.com/apis/library/sheets.googleapis.com?q=sheets&id=739c20c5-5641-41e8-a938-e55ddc082ad1&project=quickstart-1616971299388) to enable Google Sheets API for your google account.
2. Create a service account under GCP Credentials [HERE](https://console.cloud.google.com/apis/credentials).
3. Go to the sheet of interest and "Share" it with this service account, for this account to be accessible.
4. Download the credentials json from the dashboard and initialise the following env variable on your server with the json file's content : *GOOGLE_CREDENTIALS*

**If running locally:**
1. Follow this [link](https://developers.google.com/sheets/api/quickstart/python) to set up your google account.
2. Choose "desktop app" while generating the credentials json file.
3. Download the generated json file and initialise the following env variable in your **.env** file : *GOOGLE_CREDENTIALS_JSON*.
4. On first run, you will be redirected to Google's login page and asked to permit the usage of Google Sheets API.

## Setting up env variables
Initialize the following environment variables in your ecosystem, apart from the Google credentials env variable initialised from the above section. (**.env** file in root folder if running locally)
1.  **ADMIN_USERNAME** : username for accessing application
2.  **ADMIN_PASSWORD**: password for accessing application
3.  **SPREADSHEET_ID** : the value marked by "xxx...xx" in this sample Google Sheets URL ```https://docs.google.com/spreadsheets/d/xxxxxxxxxxxxxxx/edit```
4.  **RANGE_NAME** : name of the sheet of interest inside the Google sheet.


# Running the app
#### Checkout the repo and set up Virtualenv
1.  `git clone git@github.com:terriblebassist/investscape-dash.git`
2.  `cd investscape-dash`
3.  `virtualenv venv`
4.  `source venv/bin/activate`

#### Install dependencies and run app
1.  `pip install -r requirements.txt`
2.  `python app.py`


# Here's how it looks!
##### username :  ```test```  
##### password :  ```test1234```  
Sample Heroku deployment [HERE](https://investscape-dash-int.herokuapp.com)