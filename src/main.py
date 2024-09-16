import os
from datetime import datetime
from back.getNews import get_news_urls_from_bbc, get_article_n_img_from_url


if __name__ == "__main__":
    N = 3  # number of articels to crawl
    urls = get_news_urls_from_bbc(n=N)
    
    for idx, url in enumerate(urls):
        article, img_url = get_article_n_img_from_url(url)
        
        if article:
            with open(os.path.join("tmp-data", f"{str(datetime.now().strftime("%Y-%m-%d"))}-{idx}.txt"), "w", encoding="utf-8") as file:
                file.write(article)
        
        if img_url:
            with open(os.path.join("tmp-data", f"{str(datetime.now().strftime("%Y-%m-%d"))}-{idx}-img.txt"), "w", encoding="utf-8") as file:
                file.write(img_url)