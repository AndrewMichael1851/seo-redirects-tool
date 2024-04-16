# URL Checker
# Description: This tool will create a spreadsheet detailing the HTTP responses of a list of inputted URLs to look for redirects.
# Note: This program expects an input of a CSV with one column of URLs, no headers.

import csv
import requests

# Set globals
csv_data_to_write = [['original url', 'http status', 'response history']]

# Worker function to turn returned URLs into a neat list
def redirect_history(history):
    URLs = []
    for response in history:
        URLs.append(response.url)

    history = ' -> '.join(URLs)
    
    return history

# Parse the csv file of redirects
def parse_file(filename='redirects.csv'):
    with open(filename, 'r', encoding='utf-8-sig') as redirect_file:
        reader = csv.reader(redirect_file, delimiter=',')

        # Main loop for CSV
        for line in reader:
            source_url = line[0]
            response_status_code = ''
            response_history = ''

            csv_row_to_write = []

            csv_row_to_write.append(source_url)

            try:
                response = requests.head(source_url, allow_redirects = True, timeout = 12)
            
            except Exception as e:
                response = None

            if response != None:
                response_status_code = response.status_code
                response_history = redirect_history(response.history)

            csv_row_to_write.append(response_status_code)
            csv_row_to_write.append(response_history)
            print(csv_row_to_write)

            csv_data_to_write.append(csv_row_to_write)

# Write the results to a new CSV
def write_results():
    with open('redirects_results.csv', 'w') as fp: # FP as 'file pointer'
        a = csv.writer(fp, delimiter=',')
        a.writerows(csv_data_to_write)

# Start the program
parse_file()

# Write the results
write_results()