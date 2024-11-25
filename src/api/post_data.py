import os
import requests
from datetime import datetime
from .constant import API_BASE, ADD_ARTICLE_API, ADD_AUDIO_API, GET_MAX_ID_API, GET_DAILY_VISITS


# Anvil API 엔드포인트 URL
api_base = API_BASE
add_article_api = ADD_ARTICLE_API
add_audio_api = ADD_AUDIO_API
get_max_id_api = GET_MAX_ID_API


def post_data_to_server(now_date, data_path):
    """
    생성한 데이터를 news-ease 서버에 전송합니다.
    """
    dir_list = os.listdir(data_path)
    
    for dir in dir_list:
        if now_date in dir: # 오늘 날짜의 폴더에 대해서만 수행
            origin_path = os.path.join(data_path, dir)
            print(f">> API 작업 디렉토리 : {origin_path}")
            
            post_data = dict()
            
            # 공통 데이터를 딕셔너리에 저장
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
                print(f"response: {response.status_code}")  
                if response.status_code == 200:
                    data = response.json()
                    print("Max ID:", data['max_id'])
                    post_data["id"] = data["max_id"] + 1
                    
            except Exception as e:
                print(f"[Error] max_id를 받아오는 과정에서 에러가 발생하였습니다: {e}")
            
            files = os.listdir(origin_path)
            leveled_article_txt = [file for file in files if 'article-' in file and file.endswith('.txt')]
            
            # for문을 돌며 레벨별 데이터를 딕셔너리에 저장 및 전송
            for level_txt in leveled_article_txt:
                post_data["level"] = int(level_txt[-5])
                
                with open(os.path.join(origin_path, level_txt), 'r', encoding='utf-8') as file:
                    post_data["leveld_article"] = file.read()
                    
                with open(os.path.join(origin_path,level_txt[:-3] + "mp3"), 'rb') as file:
                    audio_data = file.read()
            
                    json_data = {
                        "title_id": post_data["id"],
                        "title": post_data["title"],
                        "level": post_data["level"],
                        "article": post_data["leveld_article"],
                        "img_url": post_data["img-url"],
                        "origin_url": post_data["url"],
                        "abstract": post_data["abstract"],
                    }

                    # HTTP POST 요청 보내기 (json 메타데이터 전송)
                    response = requests.post(
                        url=add_article_api, 
                        json=json_data, 
                    )
                    
                    # 응답 확인
                    if response.status_code == 200:
                        print("Adding article is Success:", response.json())
                    else:
                        print("Error:", response.status_code, response.text)
                    
                    # 오디오 파일 전송
                    print(add_audio_api + f"?title_id={post_data["id"]}&level={post_data["level"]}")
                    response = requests.post(
                        url=add_audio_api + f"?title_id={post_data["id"]}&level={post_data["level"]}", 
                        data=audio_data, 
                        headers={'Content-Type': 'application/octet-stream'},
                    )

                    # 응답 확인
                    if response.status_code == 200:
                        print("Updating audio is Success:", response.json())
                    else:
                        print("Error:", response.status_code, response.text)
