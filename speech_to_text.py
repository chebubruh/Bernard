import telebot
import os
from pydub import AudioSegment
import openai


def voice_converter(downloaded_file):
    try:
        with open("audio.ogg", 'wb') as new_file:
            new_file.write(downloaded_file)

        # конвертация файла
        ogg_audio = AudioSegment.from_file("audio.ogg", format="ogg")
        ogg_audio.export("audio.mp3", format="mp3")

        # удаление файла
        file = "audio.ogg"
        os.remove(file)

        # конвертация голоса в текст
        try:
            with open("audio.mp3", "rb") as audio_file:
                transcript = openai.Audio.transcribe("whisper-1", audio_file)

            file_mp3 = "audio.mp3"
            os.remove(file_mp3)  # удаление файла

            return transcript.text
        except telebot.apihelper.ApiTelegramException:
            file_mp3 = "audio.mp3"
            os.remove(file_mp3)

            return 'Прошу прощения, но я вас не понял, повторите пожалуйста'

    except:
        try:
            file_mp3 = "audio.mp3"
            os.remove(file_mp3)
        except:
            pass
