import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from newsapi import NewsApiClient
from openai import OpenAI

load_dotenv(verbose=True)
client = OpenAI(api_key=os.getenv("openaiAPI"))

def get_news_urls(n: int=30):
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
        
    # extract url from article lists
    article_urls = [article['url'] for article in top_headlines['articles']]  
    return article_urls
    
    
def get_article_txt_from_url(url):
    # get HTML content of url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # select p tag to get content
    paragraphs = soup.find_all('p')
    
    # join all text to one string
    article_text = '\n'.join([para.get_text() for para in paragraphs])
    return article_text


def convert_txt_to_steps(context: str, level: str):
    
    # set prompt for gpt model
    prompt = f"Rewrite the following article at a {level} level: {context}"
    
    # get response form gpt model
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that rewrites articles."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2048,
        temperature=0.5
    )
    
    # return response text
    response_dict = response.model_dump()
    response_message = response_dict["choices"][0]["message"]["content"]
    return response_message

    
if __name__ == "__main__":
    article_urls = get_news_urls(n=1)
    
    for idx, url in enumerate(article_urls, start=1):
        print(f"Fetching article {idx} from {url}")
        article_txt = get_article_txt_from_url(url)
        print(f"Article {idx} text: \n{article_txt[:500]}...")
        print("-" * 80)
        
        proficiency_level = ["elementary school", "middle-high school", "university"]
        for level in proficiency_level:
            converted_txt = convert_txt_to_steps(context=article_txt, level=level)
            print(f"Article {idx} text: \n{converted_txt[:500]}...")  
            with open(f"{level}.txt", "w", encoding="utf-8") as file:
                file.write(converted_txt)
                print("File is successfully saved ... !")
            print("o" * 20)
            
            