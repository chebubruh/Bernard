import os
import openai


def voice_converter():
    try:
        # конвертация голоса в текст
        try:
            with open("voices/voice_message.mp3", "rb") as audio_file:
                transcript = openai.Audio.transcribe("whisper-1", audio_file)

            # удаление файла mp3
            file_mp3 = "voices/voice_message.mp3"
            os.remove(file_mp3)

            return transcript.text

        except:
            file_mp3 = "voices/voice_message.mp3"
            os.remove(file_mp3)

            return 'Прошу прощения, но я вас не понял, повторите пожалуйста'

    except:
        try:
            file_mp3 = "voices/voice_message.mp3"
            os.remove(file_mp3)
        except:
            pass
