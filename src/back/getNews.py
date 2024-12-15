import os
import requests
from typing import List, Tuple
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from newsapi import NewsApiClient


def get_news_metainfo_from_bbc(n: int = 5) -> List[str]:
    """
    NewsApiClient를 사용하여 BBC의 그날 대표 뉴스 n개에 대한 메타 정보를 반환합니다.
    """
    # set tokens for NewsAPI
    # load_dotenv(verbose=True) # only for local test
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        raise ValueError("NEWS_API_KEY is not set or is empty")
    
    newsapi = NewsApiClient(api_key=api_key)
    
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
    """
    입력받은 URL을 토대로 기사의 본문 태그를 찾아 본문 내용을 반환합니다.
    """
    # get HTML content of url
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # select p tag to get content
    paragraphs = soup.find_all('p')
    article_text = '\n'.join([para.get_text() for para in paragraphs])
    
    return article_text
