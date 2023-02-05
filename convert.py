import speech_recognition as sr
import subprocess
import os

class Converter:

    def __init__(self, path_to_file: str, language: str = "uk-UK"):
        self.language = language
        subprocess.run(['ffmpeg', '-v', 'quiet', '-i', path_to_file, path_to_file.replace(".ogg", ".wav")])
        self.wav_file = path_to_file.replace(".ogg", ".wav")

    def audio_to_text(self) -> str:
        r = sr.Recognizer()

        with sr.AudioFile(self.wav_file) as source:
            audio = r.record(source)
            r.adjust_for_ambient_noise(source)
        try:
            return r.recognize_google(audio, language=self.language)

        except sr.UnknownValueError:
            return('Error: Я не зміг розпізнати аудіо.')

    def __del__(self):
        os.remove(self.wav_file)