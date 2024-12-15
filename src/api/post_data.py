import os
from nltk.corpus import wordnet
import nltk
import requests
from datetime import datetime
from .constant import API_BASE, ADD_ARTICLE_META_API, ADD_ARTICLE_LEVEL_API, ADD_AUDIO_API, ADD_WORD_API, GET_MAX_ID_API, CHECK_WORD_EXIST, GET_MAX_WORD_ID

# Anvil API 엔드포인트 URL
api_base = API_BASE
add_article_meta_api = ADD_ARTICLE_META_API
add_article_level_api = ADD_ARTICLE_LEVEL_API
add_audio_api = ADD_AUDIO_API
add_word_api = ADD_WORD_API
check_word_exist_api = CHECK_WORD_EXIST
get_max_word_id_api = GET_MAX_WORD_ID
get_max_id_api = GET_MAX_ID_API

nltk.download('wordnet')

def get_word_mean_n_synsets(word: str):
    """
    단어의 뜻과 유의어를 찾아서 반환합니다
    """
    meaning_value = ""
    synonyms_value = ""

    synonyms_list = set()
    synsets = wordnet.synsets(word)

    if len(synsets) != 0:    
        for idx, synset in enumerate(synsets):
            if idx == 0:
                meaning_value = synset.definition()
            synonyms_list.update([lemma.name() for lemma in synset.lemmas()])
        synonyms_list.discard(word) # delete original word
        synonyms_value = (", ".join(list(synonyms_list)))

    return meaning_value, synonyms_value


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
                
            with open(os.path.join(origin_path, "category.txt"), 'r', encoding='utf-8') as file:
                post_data["category"] = file.read()
            
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
                
            # 메타 데이터 전송
            json_metadata = {
                "title_id": post_data["id"],
                "title": post_data["title"],
                "category": post_data["category"],
                "img_url": post_data["img-url"],
                "origin_url": post_data["url"],
                "abstract": post_data["abstract"]
            }
            response = requests.post(url=add_article_meta_api, json=json_metadata)
            if response.status_code == 200:
                print("Adding article is Success:", response.json())
            else:
                print("Error:", response.status_code, response.text)
            
            files = os.listdir(origin_path)
            leveled_article_txt = [file for file in files if 'article-' in file and file.endswith('.txt')]
            
            # for문을 돌며 레벨별 데이터를 딕셔너리에 저장 및 전송
            for idx, level_txt in enumerate(leveled_article_txt):
                post_data["level"] = int(level_txt[-5])
                
                with open(os.path.join(origin_path, level_txt), 'r', encoding='utf-8') as file:
                    post_data["leveld_article"] = file.read()
                
                with open(os.path.join(origin_path, f"keywords-{idx + 1}.txt"), 'r', encoding='utf-8') as file:
                    tmp_str = (file.read()).replace(" ", "")
                    if '["' in tmp_str or "['" in tmp_str:
                        post_data["keywords"] = eval(tmp_str)
                    else:
                        tmp_str = tmp_str.replace("[", '["').replace("]", '"]').replace(",", '","')
                        post_data["keywords"] = eval(tmp_str)
                    
                # 단어별 DB 전송
                for word in post_data["keywords"]:
                    meaning_value, synonyms_value = get_word_mean_n_synsets(word)
                    
                    # 뜻을 찾지 못한 경우에는 단어 사전에서 제외
                    if meaning_value == "":
                        continue
                    
                    # word_id 설정
                    response = requests.get(get_max_word_id_api)
                    max_word_id = response.json().get("max_word_id")
                    word_id = max_word_id + 1
                
                    json_worddata = {
                        "title_id": post_data["id"],
                        "level": post_data["level"],
                        "word_id": word_id,
                        "word": word,
                        "meaning": meaning_value,
                        "synonyms": synonyms_value
                    }
                    response = requests.post(url=add_word_api, json=json_worddata)
                    if response.status_code == 200:
                        print(f"Adding word [{word}] is Success:", response.json())
                    else:
                        print("Error:", response.status_code, response.text)
                    
                with open(os.path.join(origin_path,level_txt[:-3] + "mp3"), 'rb') as file:
                    audio_data = file.read()
            
                    # 레벨별 기사 내용 전송
                    json_leveldata = {
                        "title_id": post_data["id"],
                        "article": post_data["leveld_article"],
                        "level": post_data["level"]
                    }
                    response = requests.post(url=add_article_level_api, json=json_leveldata)                    
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
                    if response.status_code == 200:
                        print("Updating audio is Success:", response.json())
                    else:
                        print("Error:", response.status_code, response.text)
                        
                    
