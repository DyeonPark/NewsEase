from gtts import gTTS

with open("../elementary school.txt", "r", encoding="utf-8") as file:
    text = file.read()
    
tts = gTTS(text=text, lang="en")

tts.save("elementary school.mp3")