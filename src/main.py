import os
from datetime import datetime
from back.getNews import get_news_urls_from_bbc, get_article_n_img_from_url
from back.createTTS import create_tts_from_txt
from back.createNews import convert_txt_to_steps


def check_n_crate_folder(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"디렉토리를 생성하였습니다 : {path}")
        return
    
    print(f"디렉토리가 이미 존재합니다 : {path}")
    return


def get_title_id_with_n(n: int) -> int:
    today_date = datetime.now().strftime('%Y%m%d')
    if n < 10:
        return_date = f"{today_date}0{n}"
    else:
        return_date = f"{today_date}{n}"
    return int(return_date)
        

if __name__ == "__main__":
    # get article urls from NewsAPI
    data_path = "tmp-data"
    N = 1
    urls = get_news_urls_from_bbc(n=N) 
    
    # get texts and image urls from news url
    for idx, url in enumerate(urls):
        # set directory for temp data save
        now_date_n_num =f"{str(datetime.now().strftime("%Y-%m-%d"))}-{idx}"
        save_dir = os.path.join(data_path, now_date_n_num)
        check_n_crate_folder(os.path.join(save_dir))
        
        with open(os.path.join(save_dir, "url.txt"), "w", encoding="utf-8") as file:
            file.write(url)
        
        # get article and image url
        article, img_url = get_article_n_img_from_url(url)
        
        if article:
            with open(os.path.join(save_dir, "article.txt"), "w", encoding="utf-8") as file:
                file.write(article)
        
        if img_url:
            with open(os.path.join(save_dir, "img-url.txt"), "w", encoding="utf-8") as file:
                file.write(img_url)
    
    # base variable for checking today directory
    now_date = str(datetime.now().strftime("%Y-%m-%d"))
    dir_list = os.listdir(data_path)
    news_level = {
        1: "elementary school",
        2: "middle and high school",
        3: "university"
    }
    
    # create article with levels in tmp-data folder
    for dir in dir_list:
        if now_date in dir:
            origin_path = os.path.join(data_path, dir)
            print(f">>> 기사 생성 작업 디렉토리 : {origin_path}")
            
            with open(os.path.join(origin_path, 'article.txt'), 'r', encoding='utf-8') as file:
                file_content = file.read()
                
                for level in [1, 2, 3]:
                    leveled_text = convert_txt_to_steps(context=file_content, level=news_level[level])
                    print(f">>> >>> 재생성 진행중인 기사 파일: {os.path.join(origin_path, f"article-{level}.txt")}")
                    
                    with open(os.path.join(origin_path, f"article-{level}.txt"), "w", encoding="utf-8") as file:
                        file.write(leveled_text)
                    
            
    # create tts file of today
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
                print(f">>> >>> TTS 파일 생성 완료 !! {article_path}")
    
    # post all data to Anvil NewsEase
    