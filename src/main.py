import os
from datetime import datetime
from back.getNews import get_news_metainfo_from_bbc, get_article_from_url
from back.createTTS import create_tts_from_txt
from back.createNews import convert_txt_to_steps
from api.post_data import post_data_to_server


def check_n_crate_folder(path: str) -> None:
    """입력받은 폴더 경로를 토대로 경로의 유무를 체크하고, 없다면 해당 경로를 새로 생성합니다.
    """
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
    N = 5
    articles = get_news_metainfo_from_bbc(n=N) 
    
    # get texts and image urls from news url
    for idx, item in enumerate(articles):
        # set directory for temp data save
        now_date_n_num =f"{str(datetime.now().strftime("%Y-%m-%d"))}-{idx}"
        save_dir = os.path.join(data_path, now_date_n_num)
        check_n_crate_folder(os.path.join(save_dir))
        
        with open(os.path.join(save_dir, "title.txt"), "w", encoding="utf-8") as file:
            file.write(item["title"])
            
        with open(os.path.join(save_dir, "abstract.txt"), "w", encoding="utf-8") as file:
            file.write(item["description"])
            
        with open(os.path.join(save_dir, "img-url.txt"), "w", encoding="utf-8") as file:
            file.write(item["urlToImage"])
        
        with open(os.path.join(save_dir, "url.txt"), "w", encoding="utf-8") as file:
            file.write(item["url"])
        
        # get article and image url
        article = get_article_from_url(item["url"])
        
        if article:
            with open(os.path.join(save_dir, "article.txt"), "w", encoding="utf-8") as file:
                file.write(article)
        
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
    now_date = str(datetime.now().strftime("%Y-%m-%d"))
    post_data_to_server(now_date, data_path)