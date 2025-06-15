from newsapi import NewsApiClient
import pandas as pd
import re
import os
from dotenv import load_dotenv
load_dotenv('/Users/ashfi/code/new_python/sentrade/token.env') # Replace with your own path
NEWS_API = os.getenv("NEWS_API")

newsapi = NewsApiClient(api_key=NEWS_API)

user_input = input('Search stock news: ').strip()


stock_news = newsapi.get_everything(q=user_input)


flat = pd.json_normalize(stock_news['articles'], sep='_')


safe_name = re.sub(r'[^A-Za-z0-9_]+', '_', user_input.strip())[:50]

flat.to_csv(f'{safe_name}_reviews.csv', index=False)

from newsdataapi import NewsDataApiClient
api = NewsDataApiClient(apikey='pub_f9bf033396e548cfb9f97a17e50ed4a9')
response = api.news_api(q='pizza', timeframe='') 
print(response)