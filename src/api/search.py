from constant import GET_DAILY_VISITS
import requests

def get_daily(date: str):
    # 요청 보내기
    response = requests.post(GET_DAILY_VISITS, params={"date": date})
    print(response.status_code)
    print(response.text)

    # 결과 출력
    if response.status_code == 200:
        print("Count of events:", response.json().get("count"))
        print("Logs of events:", response.json().get("logs"))
    else:
        print("Error:", response.json().get("error"))


if __name__=="__main__":
    date = "20241126"
    get_daily(date)