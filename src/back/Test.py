import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.bbc.com/news/articles/c1epe546p5vo")

soup = BeautifulSoup(response.text, "html.parser")

# data-component="image-block"을 가진 div 찾기
image_block_div = soup.find('div', {'data-component': 'image-block'})

test_id_div = image_block_div.find("div", {"data-testid": True})

img_tag = test_id_div.find("img", {"srcset": True})

srcset = img_tag.get("srcset")
urls = [url.strip() for url in srcset.split(',')]

url_480w = None
for url in urls:
    if '480w' in url:
        # 480w URL을 찾았으므로 앞의 URL을 사용
        url_480w = url.split(' ')[0]
        break

if url_480w:
    print("Extracted URL:", url_480w)
else:
    print("No URL with 480w found.")
