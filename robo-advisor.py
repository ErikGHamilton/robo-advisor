import csv
import json
import statistics
from datetime import datetime
import os
from dotenv import load_dotenv
import requests

load_dotenv() 

API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY", "demo")

company_list_csv = os.path.join(os.path.dirname(__file__), "..", "data", "companylist.csv")

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
    writingcsv = "data/" + stockdate        #TODO turn to os
    write_csv_file_path = writingcsv
    #stockdate = stockdate + ".csv"
    #write_csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", stockdate)
    #write_csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "stockdata.csv")
    with open(write_csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
        writer = csv.DictWriter(csv_file, fieldnames=["Day", "Open", "High", "Low", "Close", "Volume"])
        writer.writeheader() # uses fieldnames set above
        for w in wrows:
            writer.writerow({"Day": w["Day"], "Open": w["Open"], "High": w["High"], "Low": w["Low"], "Close": w["Close"], "Volume": w["Volume"]})

def check_input(stock_choice):    #STILL NEEDS CHARACTER NUMBER CHECKER - update 6/23 - using the company list csv
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
    
def check_input2(stock_choice): 
    df = pandas.read_csv(company_list_csv)
    companies = df.to_dict("records")
    symbols = [r['Symbols'] for r in companies]
    stock_choice = stock_choice.upper()
    if stock_choice in companies
        return("Pass")
    else:
        print("Invalid Stock Ticker Detected, Please Try Again Later")
        exit()

def request_data(stock_choice):
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_choice}&apikey={API_KEY}"
    #request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"
    response = requests.get(request_url)
    #FIGURE OUT A WAY TO TELL IF THE STOCK IS REAL OR NOT
    parsed_response = json.loads(response.text)  
    return(parsed_response)

def get_reco(recorows, recenthigh):
    avgclose = []
    for r in recorows:
        avgclose.append(r["Close"])
    avgclose = statistics.mean(avgclose)

    if recorows[0]["Close"] > recorows[10]["Close"]:
        percent_increase = 100 * ((recorows[0]["Close"] - recorows[10]["Close"]) / recorows[10]["Close"])
        percent_increase = round(percent_increase,2)
        #print(percent_increase)
    else:
        percent_increase = 0

    if recorows[0]["Close"] < recenthigh:
        percent_frommax = -100 * ((recorows[0]["Close"] - recenthigh) / recenthigh)
        percent_frommax = round(percent_frommax,2)
        #print(percent_frommax)
    else:
        percent_frommax = 0
    
    reco_list = [avgclose, percent_increase, percent_frommax]
    return(reco_list)






# BEGIN USER INTERFACE

print("------------------------------------------------------------------")
print("Welcome to Robo Advisor. I am Robo Advisor, Your Robot Advisor Pal")
print("------------------------------------------------------------------")
print("")
print("Please Input a Stock You Would Like To Analyze")

stock_choice = input()
check_input2(stock_choice) #send to stock checker
parsed_response = request_data(stock_choice)
rows = organize_response(parsed_response)  #The organized rows

meta_data = parsed_response['Meta Data']
stockdate = stock_choice + today
write_csv_function(rows,stockdate)  #Sends to go be written by the csv writer

recentlow = []
recenthigh = []
for r in rows:
    recentlow.append(r["Low"])
    recenthigh.append(r["High"])
recentlow = min(recentlow)
recenthigh = max(recenthigh)

print("You chose " + stock_choice.upper() + "! Excellent Choice! Well Done. Top Marks")
print("")
print("This program was run on " + today + " at " + hour)
print("- The Stock Data was last refreshed on " + meta_data['3. Last Refreshed'] + " -")
print("")

print("Here Are The Stats for " + stock_choice.upper() + ":")
print("")
print("Recent Close: $" + str(rows[0]['Close']))     #TODO - Transform to USD
print("Recent High: $" + str(recenthigh))
print("Recent Low: $" + str(recentlow))

print("------------------------------------------------------------------")
print("Your Robo Advisor Recommendation Is To:... ")
reco_list = get_reco(rows, recenthigh)
if rows[0]["Close"] < reco_list[0] or "0" in reco_list:
    print("Do Not Buy")
    recommendation = "DontBuy"
else:
    print("BUY BUY BUY BUY BUY")
    recommendation = "Buy"

print("") 
print("------------------------------------------------------------------")
if recommendation == "Buy":
    print("Your Robo Advisor Recommends This Because: ")
    print("The Current Closing Price of $" + str(rows[0]["Close"]) + " Is Above The Recent Average of $" + str(round(reco_list[0],2)))
    print("But Is Below The Recent High of $" + str(recenthigh) + " By " + str(reco_list[2]) + "%")
    print("And Has Shown Strong Bullish Behavior Lately By Increasing " + str(reco_list[1]) + "% In The Past 10 Days")
    print("")
    print("Given That The Stock Is Discounted From It's Recent Highs But Is Increasing In Price")
    print("Your Friendly Robo Advisor Recommends That You BUY")
else:
    print("Your Robo Advisor Recommends This Because The Stock Does Not Meet Our")
    print("Criteria of a Discounted Stock Showing Recent Bullish Behavior")
print("") 
print("------------------------------------------------------------------")