from gtts import gTTS


def create_tts_from_txt(path: str) -> None:
    """
    입력받은 텍스트 파일 경로를 사용하여, 동일한 경로의 같은 파일 이름으로 TTS(Text to speech) mp3 파일을 생성합니다.
    """
    with open(path, "r", encoding="utf-8") as file:
        text = file.read()
        tts = gTTS(text=text, lang="en")
        tts.save(f"{path[:-4]}.mp3")