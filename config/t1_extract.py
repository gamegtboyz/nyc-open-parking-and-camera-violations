def extract():
    import requests
    import pandas as pd

    from config.token import token

    ### DATA EXTRACTION ###
    # setup endpoints and API key
    endpoints = "https://data.cityofnewyork.us/resource/nc67-uf89.json"
    token = token

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

    # exported the cleaned data onto new .csv files
    data.to_csv('data/data.csv',index = False)
    print(f"{i} page(s) of dataset were downloaded successfully.")