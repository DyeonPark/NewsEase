import os
from datetime import datetime
from back.getNews import get_news_urls_from_bbc, get_article_n_img_from_url
from back.createTTS import create_tts_from_txt


def check_n_crate_folder(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"디렉토리를 생성하였습니다 : {path}")
        return
    
    print(f"디렉토리가 이미 존재합니다 : {path}")
    return


if __name__ == "__main__":
    # get article urls from NewsAPI
    data_path = "tmp-data"
    # N = 3
    # urls = get_news_urls_from_bbc(n=N) 
    
    # # get texts and image urls from news url
    # for idx, url in enumerate(urls):
    #     # set directory for temp data save
    #     now_date_n_num =f"{str(datetime.now().strftime("%Y-%m-%d"))}-{idx}"
    #     save_dir = os.path.join(data_path, now_date_n_num)
    #     check_n_crate_folder(os.path.join(save_dir))
        
    #     # get article and image url
    #     article, img_url = get_article_n_img_from_url(url)
        
    #     if article:
    #         with open(os.path.join(save_dir, "article.txt"), "w", encoding="utf-8") as file:
    #             file.write(article)
        
    #     if img_url:
    #         with open(os.path.join(save_dir, "img-url.txt"), "w", encoding="utf-8") as file:
    #             file.write(img_url)
                
    # create articles with levels in folder
    
    
    # create tts file of today
    now_date = str(datetime.now().strftime("%Y-%m-%d"))
    dir_list = os.listdir(data_path)
    
    for dir in dir_list:
        if now_date in dir:
            tts_path = os.path.join(data_path, dir)
            print(f">>> 작업 디렉토리 : {tts_path}")
            
            file_list = os.listdir(tts_path)
            article_list = [file for file in file_list if file.startswith('article-') and file.endswith('.txt')]
            for article in article_list:
                article_path = os.path.join(tts_path, article)
                print(f">>> >>> TTS 파일 생성중: {article_path}")
                create_tts_from_txt(article_path)
    
    # post all data to Anvil NewsEase
    