import requests
import pandas as pd
import json
import datetime as dt
import ast

### DATA EXTRACTION ###
# setup endpoints and API key
endpoints = "https://data.cityofnewyork.us/resource/nc67-uf89.json"
token = "qMLbbltM4PxnOZ6W4yZgE3QIO"

# define parameters
params = {
    '$limit' : 10000,
    '$offset' : 0,
    '$where' : 'issue_date >= "2024-01-01T00:00:00"',
    '$order' : 'issue_date DESC',
}

# set headers, using defined token
headers = {
    'X-App-Token' : token
}

# fetch data, using defined endpoints, headers, and params
all_data = []
i = 0
while True:
    # get the response from request
    response = requests.get(endpoints,headers = headers, params = params)

    # if the response return 200, extract the data as json format
    if response.status_code == 200:
        data = response.json()

        # if the reponse == 200, but there's no more data, then break it 
        if not data:
            break

        # if theey still have an data, just extend it, offset with the length of downloaded data, and append it
        all_data.extend(data)
        params['$offset'] += len(data)
        i += 1
        print(f'fetching ({i})')
    
    # if the response return something else but 200, just return an error
    else:
        print(f'Error: {response.status_code}, {response.text}')
        break

# convert the downloaded data from json to DataFrame, then export it into .csv files
data = pd.DataFrame(all_data)

### DATA TRANSFORMATION ###
'''
From data extractions, we saw the something in the dataset which needs to be transformed before loading into database
1. Some rows in 'issue_date' shows the odd date. we need to transform into timestamp, and drop the odd date.
2. Some value in 'state' and 'license_type' shows as '99' and '999', respectively. we need to drop it.
3. 'summon_image' shows the strings which looks like dictionary. We need only url links for memory optimization purpose.
4. 'violation_time' string format is kinda odd. We need to drop some observations which is unreadable, then transform it into timestamp
'''

## 1. 'issue_date' data transformation ##
# drop the odd date format, which is also the odd date, from the dataset
regex = r"^\d{2}/\d{2}/\d{4}$"
data = data[~data['issue_date'].str.match(regex)]

# split the 'issue_date' into date and time. Since the time is only shows 00:00, we will drop those column also
data[['issuance_date','issuance_time']] = data['issue_date'].str.split('T', expand=True)
data.drop('issuance_time', axis=1, inplace=True)

# transform 'issuance_date' into python timestamp form
data['issuance_date'] = pd.to_datetime(data['issuance_date'],format='%Y-%m-%d')

# filter out the future dates.
today = pd.to_datetime(dt.date.today())     # we need to call for date of today, which is in form of datetime[64] first, then convert it into timestamp format for comparability purpose
data = data[data['issuance_date'] <= today] # filter out the future dates

## 2. 'violation_time' data transformation ##
# based on our review in datasets, we have to transform the observation with particular string pattern into timestamp format
regex_vtime = r"^(0[0-9]|1[0-2]):([0-5][0-9])[AP]$"
data = data[data['violation_time'].str.match(regex_vtime)]
data['violation_time'] = pd.to_datetime(data['violation_time']).dt.time

## 3. 'summon_image' data transformation ##
# we will convert dictionary-like strings into actual dictionary and put it into the new columns
data['summons_image'] = data['summons_image'].apply(ast.literal_eval)
data['image_url'] = data['summons_image'].apply(lambda x: x.get('url',None))

## 4. 'license_type' transformation ##
data = data[(data['license_type'] != '999') | (data['state'] != '99')]

# exported the cleaned data onto new .csv files
data.to_csv('src_open_parking_and_camera_violations.csv',index = False)
print(f"{i} page(s) of dataset were downloaded successfully.")