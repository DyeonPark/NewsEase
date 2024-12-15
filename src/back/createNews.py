import os
import requests
from typing import List, Tuple
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(verbose=True) # only for local test
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set or is empty")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def process_string(message: str):
    if message.find('category"=') >= 0:
        print(">>> category 데이터의 =를 :로 변경합니다")
        message = message.replace('category"=', 'category":')
    
    if message.find('category"=') >= 0:
        print(">>> category 데이터의 =를 :로 변경합니다")
        message = message.replace('category"=', 'category":')
        
    if message.find('keywords"=') >= 0:
        print(">>> keywords 데이터의 =를 :로 변경합니다")
        message = message.replace('keywords"=', 'keywords":')
    
    if message.find("```json") >= 0:
        message = message.replace("```json", "")
    
    if message.find("```") >= 0:
        message = message.replace("```", "")
    
    return message

def convert_txt_to_steps(context: str, level: str):
    """
    입력받은 기사 내용(context)을 입력받은 수준(level)에 맞게 재생성합니다.
    """
    
    # set prompt for gpt model
    prompt = f'''
    I'll send you the article body. Please return the value in json format like below.
    {{"rewrite_article":string , "category":string, "keywords":list(str)}}

    1. Rewrite the article text to a {level} level and put it as the first part of the return value. You must finish article within 50 centences, and line it up appropriately to make it easier to read
    2. Select the category of t]orts, business, innovation, culture, travel, or earth, and enter it as the second value in the return value.
    3. Select 5-7 important words from the article in purpose of learning English and put them as the 3rd part of the return value

    Article Text: {context}
    '''
    
    # get response form gpt model
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that rewrites articles for teaching English."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2048,
        temperature=0.5
    )
    
    # return response text
    response_dict = response.model_dump()
    response_message = response_dict["choices"][0]["message"]["content"]
    processed_message = process_string(response_message)
    return processed_message