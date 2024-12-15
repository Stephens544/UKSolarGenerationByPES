import requests
import io
import os
import pandas as pd

# API documenation: https://www.solar.sheffield.ac.uk/api/

def main():
    # Set up the URL and parameters for each PSE 
    PES_ID = [10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    for i in PES_ID:
        PES = i
        url=f"https://api.solar.sheffield.ac.uk/pvlive/api/v4/pes/{PES}"
        params = {
            'start':'2023-12-01 00:00:00',
            'end': '2024-12-01 00:00:00',
            'data_format': 'csv'
        }
        if params['data_format'] == 'csv':
            print(params['data_format'])

            headers = {
                'Content-Type': 'application/json',  
                'Accept': 'application/json'
            }
        ## Obtaining the data via the API
        try:
            # Send the GET request
            response = requests.get(url, params=params)
            
            # Check for HTTP errors
            response.raise_for_status()

            # Check if the response is empty
            if response.text.strip() == "":
                print("The response is empty.")


            # Check if we've asked for CV and if so add to DF and print
            elif params['data_format'] == 'csv':
                csv_data = response.text
                df = pd.read_csv(io.StringIO(csv_data))


            else:
                # Attempt to parse JSON response
                try:
                    data = response.json()
                    print("Response JSON data:", data)
                except ValueError as json_err:
                    print("Error parsing JSON:", json_err)
                    print("Raw response text:", response.text)  # For debugging

            
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Handle HTTP errors
        except requests.exceptions.RequestException as err:
            print(f"Error occurred: {err}")  # Handle other request errors
        except (ConnectionError) as e:
            print(e)


        ## Save the data

        df['timestamp'] = pd.to_datetime('now')

        if not os.path.isfile(r'C:\Users\HP\ProjectsForPortfolio\NationalPVGen\DataFromAPI\PSE_API_2023-2024.csv'):
            df.to_csv(r'C:\Users\HP\ProjectsForPortfolio\NationalPVGen\DataFromAPI\PSE_API_2023-2024.csv', header='column_names')
            print(f"CSV from PSE Region {i} created successfully")
        else:
            df.to_csv(r'C:\Users\HP\ProjectsForPortfolio\NationalPVGen\DataFromAPI\PSE_API_2023-2024.csv', mode='a', header=False)
            print(f"Data from PES Region {i} appended successfully")
               


main()


