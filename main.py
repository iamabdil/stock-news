import requests
import os
from twilio.rest import Client

# STOCK & NEWS VARIABLES
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = os.environ['STOCK_API_KEY']
NEWS_API_KEY = os.environ['NEWS_API_KEY']

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

# TWILIO VARIABLES
account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['AUTH_TOKEN']

# STOCKS
stock_response = requests.get(STOCK_ENDPOINT, stock_params)
stock_data = stock_response.json()['Time Series (Daily)']
data_list = [values for (key, values) in stock_data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

difference = float(day_before_yesterday_closing_price)-float(yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

percentage_difference = round((difference/float(yesterday_closing_price))*100)

# NEWS
if abs(difference) > 1:
    news_params = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API_KEY,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()['articles']
    three_articles = articles[:3]

    formatted_articles = [f"{STOCK_NAME}: {up_down}{percentage_difference}%\nHeadline: {article['title']}. \nBrief: {article['description']}\n {article['url']}" for article in three_articles]

    client = Client(account_sid, auth_token)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=os.environ['TWILIO_NUMBER'],
            to=os.environ['MY_NUMBER']
        )


