import requests

# Anvil API 엔드포인트 URL
api_url = "https://mellow-blond-external.anvil.app/_/api/add_article"

# 전송할 데이터
data = {
    "title_id": 1,
    "title": "Article title",
    "date": "2024-09-06",
    "level": 1,
    "article": "Article content sample"
}

# HTTP POST 요청 보내기
response = requests.post(api_url, json=data)

# 응답 확인
if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.status_code, response.text)
