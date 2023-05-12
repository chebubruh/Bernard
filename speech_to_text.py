import telebot
import os
from pydub import AudioSegment
import openai


def voice_converter(downloaded_file):
    try:
        with open("voices/audio.ogg", 'wb') as new_file:
            new_file.write(downloaded_file)

        # конвертация файла
        ogg_audio = AudioSegment.from_file("voices/audio.ogg", format="ogg")
        ogg_audio.export("voices/audio.mp3", format="mp3")

        # удаление файла ogg
        file = "voices/audio.ogg"
        os.remove(file)

        # конвертация голоса в текст
        try:
            with open("voices/audio.mp3", "rb") as audio_file:
                transcript = openai.Audio.transcribe("whisper-1", audio_file)

            # удаление файла mp3
            file_mp3 = "voices/audio.mp3"
            os.remove(file_mp3)

            return transcript.text
        except telebot.apihelper.ApiTelegramException:
            file_mp3 = "voices/audio.mp3"
            os.remove(file_mp3)

            return 'Прошу прощения, но я вас не понял, повторите пожалуйста'

    except:
        try:
            file_mp3 = "voices/audio.mp3"
            os.remove(file_mp3)
        except:
            pass
