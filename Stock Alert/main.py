import smtplib
import requests
from twilio.rest import Client
import os

#Stock data
STOCK = "TSLA"
STOCK_API = os.getenv("STOCK_API")
STOCK_PARAM = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK,
    "apikey" : STOCK_API,
    "outputsize" : 2,
}

#News Data
NEWS_API = os.getenv("NEWS_API")
NEWS_PARAM = {
    "q" : "tesla",
    "apikey" : NEWS_API,
}

#Twilio sms data
account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")

#Open and close stock data
OPEN = '1. open'
CLOSE = '4. close'

#Calculate percent
def calculate_percentage_change(open_price, close_price):
    if open_price == 0:
        return "Cannot divide by zero"
    percentage_change = ((close_price - open_price) / open_price) * 100
    return percentage_change

#Send mail
def sendEmail():
    sender = "sender_email"
    receiver = "receiver_email"
    password = "bjuk ydww rilv zsbe"
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
        connection.login(user=sender, password=password)
        connection.sendmail(
            from_addr=sender,
            to_addrs=receiver,
            msg='Subject:Volatile!\n'
                '\nThe stock is very volatile!!!'
        )

#Get Stock Data
request_stock = requests.get('https://www.alphavantage.co/query', params=STOCK_PARAM)
request_stock.raise_for_status()
data_stock = request_stock.json()

# Extract the last two days of stock data
time_series = data_stock["Time Series (Daily)"]
available_dates = sorted(time_series.keys(), reverse=True)[:2]
print("Available dates:", available_dates)

TODAY = available_dates[0]
YESTERDAY = available_dates[1]


#Get News Data
request_news = requests.get('https://newsapi.org/v2/everything', params=NEWS_PARAM)
request_news.raise_for_status()
data_news = request_news.json()

news_name = data_news["articles"][0]["source"]["name"]
news_title = data_news["articles"][0]["title"]
news_description = data_news["articles"][0]["description"]
news_date = data_news["articles"][0]["publishedAt"].split("T")[0]

#Get the stock prices
open_price_current_day = float(data_stock["Time Series (Daily)"][TODAY][OPEN])
close_price_current_day = float(data_stock["Time Series (Daily)"][TODAY][CLOSE])
close_price_yesterday = float(data_stock["Time Series (Daily)"][YESTERDAY][CLOSE])

current_day_percent = abs(calculate_percentage_change(open_price_current_day,close_price_current_day))
if current_day_percent > 5:
    sendEmail()

stock_percent = abs(calculate_percentage_change(close_price_yesterday,close_price_current_day))
if stock_percent >= 10:
    # Send message via Twilio sms
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="New Tesla news.\n"
             f"By {news_name}, on {news_date}\n"
             f"{news_title}\n"
             f"{news_description}\n",
        from_='+12076186472',
        to='your phone number'
    )
    print(message.status)

