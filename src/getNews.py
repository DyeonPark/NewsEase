import os
from dotenv import load_dotenv
from newsapi import NewsApiClient

load_dotenv(verbose=True)

NEWS_TOKEN = os.getenv("NewsAPI")
newsapi = NewsApiClient(api_key=NEWS_TOKEN)

print(NEWS_TOKEN)