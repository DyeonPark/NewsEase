import os
import requests
from typing import List, Tuple
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(verbose=True)
client = OpenAI(api_key=os.getenv("openaiAPI"))

def convert_txt_to_steps(context: str, level: str):
    """
    입력받은 기사 내용(context)을 입력받은 수준(level)에 맞게 재생성합니다.
    """
    
    # set prompt for gpt model
    prompt = f"Rewrite the following article at a {level} level: {context}"
    
    # get response form gpt model
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that rewrites articles."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.5
    )
    
    # return response text
    response_dict = response.model_dump()
    response_message = response_dict["choices"][0]["message"]["content"]
    return response_message
