import os
from dotenv import load_dotenv
from newsapi import NewsApiClient

load_dotenv(verbose=True)

NEWS_TOKEN = os.getenv("NewsAPI")
newsapi = NewsApiClient(api_key=NEWS_TOKEN)

# get top headlines of bbc-news
top_headlines = newsapi.get_top_headlines(sources='bbc-news', page_size=5)

# get title, description, url of articles
for idx, article in enumerate(top_headlines['articles'], start=1):
    print(f"Article {idx}:")
    print(f"Title: {article['title']}")
    print(f"Description: {article['description']}")
    print(f"URL: {article['url']}")
    print("-" * 80)