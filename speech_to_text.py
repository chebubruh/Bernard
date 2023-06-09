import os
import ffmpeg
import openai


def voice_converter():
    try:
        # конвертация файла
        stream = ffmpeg.input(os.path.abspath("voices/audio.ogg"))
        stream = ffmpeg.output(stream, os.path.abspath("voices/audio.mp3"))
        ffmpeg.run(stream)

        # удаление файла ogg
        file = os.path.abspath("voices/audio.ogg")
        os.remove(file)

        # конвертация голоса в текст
        try:
            with open(os.path.abspath("voices/audio.mp3"), "rb") as audio_file:
                transcript = openai.Audio.transcribe("whisper-1", audio_file)

            # удаление файла mp3
            file_mp3 = os.path.abspath("voices/audio.mp3")
            os.remove(file_mp3)

            return transcript.text
        except Exception as ex:
            file_mp3 = os.path.abspath("voices/audio.mp3")
            os.remove(file_mp3)

            print(ex)
            return 'Сделай вид, что ты меня не понял и попроси повторить'

    except Exception as ex:
        try:
            file_mp3 = os.path.abspath("voices/audio.mp3")
            os.remove(file_mp3)
            print(ex)
            return 'Сделай вид, что ты меня не понял и попроси повторить'
        except Exception as ex:
            print(ex)
            return 'Сделай вид, что ты меня не понял и попроси повторить'
        try:
            file_ogg = os.path.abspath("voices/audio.ogg")
            os.remove(file_ogg)
            return 'Сделай вид, что ты меня не понял и попроси повторить'
        except Exception as ex:
            print(ex)
            return 'Сделай вид, что ты меня не понял и попроси повторить'
