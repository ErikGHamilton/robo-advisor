import csv
import json
import datetime
import os

from dotenv import load_dotenv
import requests

load_dotenv() 

API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY", "demo")

def organize_response(parsed_response):
    org_response = parsed_response["Time Series (Daily)"]
    return_rows = []
    #breakpoint()
    for d, p in org_response.items():
        row = {
            "Day": d,
            "Open": float(p["1. open"]),
            "High": float(p["2. high"]),
            "Low": float(p["3. low"]),
            "Close": float(p["4. close"]),
            "Volume": float(p["5. volume"])
        }
        return_rows.append(row)
    #print(return_rows)
    return(return_rows)

def write_csv_function(wrows, write_csv_file_path):  #what do i need to input?
    with open(write_csv_file_path, "w", newline='') as csv_file: # "w" means "open the file for writing"
        writer = csv.DictWriter(csv_file, fieldnames=["timestamp", "open", "high", "low", "close", "volume"])
        writer.writeheader() # uses fieldnames set above
        #writer.writerow({"Keyword": "test", "Campaign": "test"})    TODO - Define the writing parameters


#request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}
request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"
response = requests.get(request_url)
#print(response)
#print(response.text)
parsed_response = json.loads(response.text)
print(parsed_response)
print("")

rows = organize_response(parsed_response)
#print(rows)