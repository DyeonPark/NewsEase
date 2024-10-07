import os
import requests
from typing import List, Tuple
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from newsapi import NewsApiClient
from openai import OpenAI

load_dotenv(verbose=True)
client = OpenAI(api_key=os.getenv("openaiAPI"))


def get_news_urls_from_bbc(n: int = 5) -> List[str]:
    # set tokens for NewsAPI
    NEWS_TOKEN = os.getenv("NewsAPI")
    newsapi = NewsApiClient(api_key=NEWS_TOKEN)
    
    # get top headlines of bbc-news
    top_headlines = newsapi.get_top_headlines(sources='bbc-news', page_size=n)
        
    # extract url from article lists
    article_urls = [article['url'] for article in top_headlines['articles']]  
    return article_urls
    
    
def get_article_n_img_from_url(url: str) -> Tuple[str, str]:
    # get HTML content of url
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # select p tag to get content
    paragraphs = soup.find_all('p')
    article_text = '\n'.join([para.get_text() for para in paragraphs])
    
    # find div tag with "image-block" property
    image_block_div = soup.find('div', {'data-component': 'image-block'})
    img_tag = image_block_div.find("img", {"srcset": True})
    
    srcset = img_tag.get("srcset")
    urls = [url.strip() for url in srcset.split(',')]
    
    url_480w = None
    for url in urls:
        if '480w' in url:
            # catch url infront of '480w'
            url_480w = url.split(' ')[0]
            break

    if url_480w:
        print("Extracted Image URL:", url_480w)
    else:
        print("No URL with 480w found.")
    
    return article_text, url_480w
