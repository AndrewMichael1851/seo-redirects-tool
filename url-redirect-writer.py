import csv
import requests

def check_redirects(input_csv, output_csv):
    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        writer.writerow(["Original URL", "Redirect URL"])  # Write header to output CSV

        for row in reader:
            original_url = row[0].strip('\ufeff').strip()
            try:
                response = requests.get(original_url, timeout=10)  # Timeout set to 10 seconds
                if response.history:  # Check if there were any redirects
                    redirect_url = response.url
                else:
                    redirect_url = "No redirect"  # Or some other placeholder to indicate no redirect
                writer.writerow([original_url, redirect_url])
            except requests.RequestException as e:
                print(f"Failed to process {original_url}: {e}")
                writer.writerow([original_url, "Failed to check"])  # Handle failed requests

if __name__ == "__main__":
    input_csv_path = 'redirects.csv'  # Name of the input CSV file
    output_csv_path = 'output.csv'  # Name of the output CSV file
    check_redirects(input_csv_path, output_csv_path)
