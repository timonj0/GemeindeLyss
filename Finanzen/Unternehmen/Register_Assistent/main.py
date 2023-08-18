'''Script to assist with the Zefix API'''

import time

import requests
import pandas as pd

API_URL = 'https://www.zefix.ch/ZefixREST/api/v1/firm/search.json'
TOTAL_COMPANIES = 0
REQUEST_INTERVAL = 0.2

def load_data():
    '''Loads the data from the excel file'''
    dataframe = pd.read_excel('unternehmen.xlsx')
    return dataframe


def mainloop(company_names, dataframe_original):
    '''Main loop'''
    counter = 1
    dataframe_responses = pd.DataFrame()
    for name in company_names:
        # create the payload
        payload = {
            'languageKey': 'de',
            'maxEntries': 30,
            'offset': 0,
            'name': name.upper()
        }

        formatted_name = name.replace(' ', '%20')
        headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Host': 'www.zefix.ch',
        'Origin': 'https://www.zefix.ch',
        'Referer': f'https://www.zefix.ch/de/search/entity/list?mainSearch={formatted_name}',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows'
        }

        # Send the request
        response = requests.post(API_URL, json=payload)
        
        success = False

        # Check the response
        if response.status_code == 200:
            success = True
            # Add the response to a new dataframe
            df = pd.json_normalize(response.json()['list'])

            # Check if the value for 'status' is 'EXISTIEREND' using any()
            exists = df['status'].str.contains('EXISTIEREND').any()

            if exists:
                # Remove company from 'original_df'
                dataframe_original = dataframe_original[dataframe_original['Name'] != name]

            # Add to the responses dataframe
            dataframe_responses = pd.concat([dataframe_responses, df], ignore_index=True)

        else:
            # Add a dummy response to a new dataframe
            df = pd.DataFrame({'name': [name], 'response': [response.status_code]})
            # Add to the responses dataframe
            dataframe_responses = pd.concat([dataframe_responses, df], ignore_index=True)


        # Print the status
        print(chr(27) + "[2J")
        print(dataframe_responses.tail(6))
        print("\n\n\n\n")
        print(f"{counter}/{TOTAL_COMPANIES} - {name} - {success}")
        counter += 1

        time.sleep(REQUEST_INTERVAL)


def save_data(dataframe_responses, original_df):
    '''Saves the data to an excel file'''
    dataframe_responses.to_excel('responses.xlsx', index=False)
    original_df.to_excel('unternehmen_corrected.xlsx', index=False)


def run():
    global TOTAL_COMPANIES
    '''Main function'''
    dataframe_unternehmen = load_data()
    TOTOAL_COMPANIES = len(dataframe_unternehmen)
    company_names = dataframe_unternehmen['Name'].tolist()
    dataframe_responses, dataframe_corrected = mainloop(company_names, dataframe_unternehmen)
    save_data(dataframe_responses, dataframe_corrected)
    print("Done.")

if __name__ == "__main__":
    run()