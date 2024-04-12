# URL Checker
# Description: Lorem ipsum.

import csv
import requests

csv_data_to_write = [['original url', 'destination url', 'final http status', 'redirect path']]

# Function to turn URLs into a neat list.
def redirect_history(history):
    hops = []
    for response in history:
        hops.append(response.url)

    history = ' -> '.join(hops)

    return history

# Parse the csv file of redirects and generate a results csv
def parse_file(filename='redirects.csv'):
    with open(filename, 'r', encoding='utf-8-sig') as redirect_file:
        reader = csv.reader(redirect_file, delimiter=',')

        for line in reader:
            source_url = line[0]
            destination_url = line[1]
            response_text=''
            response_status_code = ''
            response_history = ''

            csv_row_to_write = []

            csv_row_to_write.append(source_url)
            csv_row_to_write.append(destination_url)

            try:
                response = requests.head(source_url, allow_redirects = True, timeout = 12)
            
            except Exception as e:
                response = None
                response_text = e

            if response != None:
                response_status_code = response.status_code
                response_history = redirect_history(response.history)

                for hop in response.history:
                    if hop.url == destination_url:
                        response_text = 'successful'

            csv_row_to_write.append(response_text)
            csv_row_to_write.append(response_status_code)
            csv_row_to_write.append(response_history)

            csv_data_to_write.append(csv_row_to_write)

# Function to write the results
def write_results():
    with open('redirects_results.csv', 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(csv_data_to_write)

# Start the program
parse_file()

# Write the results
write_results()