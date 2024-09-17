from gtts import gTTS


def create_tts_from_txt(path: str) -> None:
    with open(path, "r", encoding="utf-8") as file:
        text = file.read()
        tts = gTTS(text=text, lang="en")
        tts.save(f"{path[:-4]}.mp3")