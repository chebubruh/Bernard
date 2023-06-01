import os
import ffmpeg
import openai


def voice_converter():
    try:
        # конвертация файла
        stream = ffmpeg.input("voices/audio.ogg")
        stream = ffmpeg.output(stream, "voices/audio.mp3")
        ffmpeg.run(stream)

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
        except:
            file_mp3 = "voices/audio.mp3"
            os.remove(file_mp3)

            return 'Сделай вид, что ты меня не понял и попроси повторить'

    except:
        try:
            file_mp3 = "voices/audio.mp3"
            os.remove(file_mp3)
            return 'Сделай вид, что ты меня не понял и попроси повторить'
        except:
            return 'Сделай вид, что ты меня не понял и попроси повторить'
        try:
            file_ogg = "voices/audio.ogg"
            os.remove(file_ogg)
            return 'Сделай вид, что ты меня не понял и попроси повторить'
        except:
            return 'Сделай вид, что ты меня не понял и попроси повторить'
