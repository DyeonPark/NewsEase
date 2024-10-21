import os
import requests
from anvil import Media
from datetime import datetime


# Anvil API 엔드포인트 URL
api_base = "https://news-ease.com/_/api/"
add_article_api_ = api_base + "add_article"
get_max_id_api = api_base + "max_id"

# 오늘 날짜의 폴더 찾기
now_date = str(datetime.now().strftime("%Y-%m-%d"))
data_path = "../tmp-data"
dir_list = os.listdir(data_path)


def format_string(input: str) -> str:
    date_part = input.split('/')[2].split('-')
    last_number = int(date_part[-1])  # 마지막 숫자 추출
    
    # 날짜 부분을 결합하고, 마지막 숫자를 두 자리로 변환
    formatted_string = f"{date_part[0]}{date_part[1]}{date_part[2]}{last_number:02d}"
    return formatted_string


for dir in dir_list:
    if now_date in dir:
        origin_path = os.path.join(data_path, dir)
        print(f">> API 작업 디렉토리 : {origin_path}")
        
        post_data = dict()
        with open(os.path.join(origin_path, "title.txt"), 'r', encoding='utf-8') as file:
            post_data["title"] = file.read()
            
        with open(os.path.join(origin_path, "url.txt"), 'r', encoding='utf-8') as file:
            post_data["url"] = file.read()
            
        with open(os.path.join(origin_path, "img-url.txt"), 'r', encoding='utf-8') as file:
            post_data["img-url"] = file.read()
            
        with open(os.path.join(origin_path, "abstract.txt"), 'r', encoding='utf-8') as file:
            post_data["abstract"] = file.read()
        
        
        max_id = 0
        try:
            response = requests.get(get_max_id_api)  
            if response.status_code == 200:
                data = response.json()
                print("Max ID:", data['max_id'])
                post_data["id"] = data["max_id"] + 1
                
        except Exception as e:
            print(f"[Error] max_id를 받아오는 과정에서 에러가 발생하였습니다: {e}")
        
        files = os.listdir(origin_path)
        leveled_article_txt = [file for file in files if 'article-' in file and file.endswith('.txt')]
        
        # 전송할 데이터
        for level_txt in leveled_article_txt:
            post_data["level"] = int(level_txt[0][-5])
            
            with open(os.path.join(origin_path, level_txt), 'r', encoding='utf-8') as file:
                post_data["leveld_article"] = file.read()
        
            data = {
                "title_id": 1,
                # "date": ,  # 테스트 필요
                "title": post_data["title"],
                "level": post_data["level"],
                "article": post_data["leveld_article"],
                # "tts_audio": ,  # 테스트 필요
                "img_url": post_data["img-url"],
                "origin_url": post_data["url"],
                "abstract": post_data["abstract"],
            }

        # # HTTP POST 요청 보내기
        # response = requests.post(api_url, json=data)

        # # 응답 확인
        # if response.status_code == 200:
        #     print("Success:", response.json())
        # else:
        #     print("Error:", response.status_code, response.text)
