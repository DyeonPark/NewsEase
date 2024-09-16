# from api.test_connection import
# from back.createTTS
import os
from datetime import datetime
from back.getNews import get_news_urls_from_bbc, get_article_txt_from_url


if __name__ == "__main__":
    N = 3  # number of articels to crawl
    urls = get_news_urls_from_bbc(n=N)
    
    for idx, url in enumerate(urls):
        article = get_article_txt_from_url(url)
        with open(os.path.join("tmp-data", f"{str(datetime.now().strftime("%Y-%m-%d"))}-{idx}.txt"), "w", encoding="utf-8") as file:
            file.write(article)