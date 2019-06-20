import csv
import json
from datetime import datetime
import os
from dotenv import load_dotenv
import requests

load_dotenv() 

API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY", "demo")

today = datetime.now().strftime('%Y-%m-%d')   #https://stackoverflow.com/questions/415511/how-to-get-the-current-time-in-python
hour = datetime.now().strftime('%H:%M')

#now = datetime.datetime.now
#today = str(now.year) + "-" + str(now.month) + "-" + str(now.day)


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

def write_csv_function(wrows, stockdate):  #what do i need to input?
    writingcsv = "data/" + stockdate
    write_csv_file_path = writingcsv
    with open(write_csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
        writer = csv.DictWriter(csv_file, fieldnames=["Day", "Open", "High", "Low", "Close", "Volume"])
        writer.writeheader() # uses fieldnames set above
        for w in wrows:
            writer.writerow({"Day": w["Day"], "Open": w["Open"], "High": w["High"], "Low": w["Low"], "Close": w["Close"], "Volume": w["Volume"]})

def check_input(stock_choice):    #STILL NEEDS CHARACTER NUMBER CHECKER
    numchar = len(stock_choice)
    #nonum = any(char.isdigit() for char in input)    #TODO MAKE THIS WORK
    nonum = "False"
    if numchar > 4:
        #return("Fail")
        print("Invalid Stock Ticker Detected, Please Try Again Later")
        exit()
    elif nonum == "True":
        #return("Fail")
        print("Invalid Stock Ticker Detected, Please Try Again Later")
        exit()
    else:
        return("Pass")
    
def request_data(stock_choice):
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_choice}&apikey={API_KEY}"
    #request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"
    response = requests.get(request_url)
    #FIGURE OUT A WAY TO TELL IF THE STOCK IS REAL OR NOT
    parsed_response = json.loads(response.text)  
    return(parsed_response)


# BEGIN USER INTERFACE

print("------------------------------------------------------------------")
print("Welcome to Robo Advisor. I am Robo Advisor, Your Robot Advisor Pal")
print("------------------------------------------------------------------")
print("")
print("Please Input a Stock You Would Like To Analyze")

stock_choice = input()
check_input(stock_choice) #send to stock checker
parsed_response = request_data(stock_choice)
rows = organize_response(parsed_response)
meta_data = parsed_response['Meta Data']
stockdate = stock_choice + today
write_csv_function(rows,stockdate)

recentlow = []
recenthigh = []
for r in rows:
    recentlow.append(r["Low"])
    recenthigh.append(r["High"])
recentlow = min(recentlow)
recenthigh = max(recenthigh)

print("You chose " + stock_choice.upper() + "! Excellent Choice! Well Done. Top Marks")
print("")
print("This program was run on " + today + "at " + hour)
print("The Data was last refreshed at " + meta_data['3. Last Refreshed'])
print("")

print("Here Are The Stats for " + stock_choice.upper() + "!")
print("Recent Close: " + str(rows[0]['Close']))     #TODO - Transform to USD
print("Recent High: " + str(recenthigh))
print("Recent Low: " + str(recentlow))

print("------------------------------------------------------------------")
print("Your Robo Advisor Recommendation Is To: ")
print("") # COME UP WITH CRITERIA
print("------------------------------------------------------------------")
print("Your Robo Advisor Recommends This Because: ")
print("") # COME UP WITH CRITERIA - Maybe it is below recent high/averages but is increasing over last 10 days?