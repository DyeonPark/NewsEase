import os
import requests
from typing import List, Tuple
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from newsapi import NewsApiClient
from openai import OpenAI

load_dotenv(verbose=True)
client = OpenAI(api_key=os.getenv("openaiAPI"))


def get_news_metainfo_from_bbc(n: int = 5) -> List[str]:
    # set tokens for NewsAPI
    NEWS_TOKEN = os.getenv("NewsAPI")
    newsapi = NewsApiClient(api_key=NEWS_TOKEN)
    
    # get top headlines of bbc-news
    top_headlines = newsapi.get_top_headlines(sources='bbc-news', page_size=n)
    
    # extract meta information from article lists
    articles = []
    for article in top_headlines['articles']:
        info_dict = dict()
        info_dict["title"] = article['title']
        info_dict["description"] = article['description']
        info_dict["url"] = article['url']
        info_dict["urlToImage"] = article['urlToImage']
        articles.append(info_dict)
        
    return articles
    
    
def get_article_from_url(url: str) -> str:
    # get HTML content of url
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # select p tag to get content
    paragraphs = soup.find_all('p')
    article_text = '\n'.join([para.get_text() for para in paragraphs])
    
    return article_text
