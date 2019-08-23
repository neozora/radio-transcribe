import requests
import os
import time
import ffmpy
import speech_recognition as sr
from os import path

chunk_size = 50000  # bytes
output_file = "output\\transcript.txt"
source_url = "http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio4fm_mf_q"
resp_timeout = 5  # secs
temp_mp3 = "temp\\audio.mp3"
temp_wav = "temp\\audio.wav"

headers = {
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/75.0.3770.100 Safari/537.36'
}


def convert(mp3, wav):
    ff = ffmpy.FFmpeg(
        global_options={"-y -loglevel panic -hide_banner"},
        inputs={mp3: None},
        outputs={wav: None}
    )
    ff.run()
    

def transcribe(source_file):
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), source_file)


    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)

    try:
        return r.recognize_sphinx(audio)
    except sr.UnknownValueError:
        return " (inaudible) "
    except sr.RequestError as e:
        return "Sphinx error; {0}".format(e)


def main(source, output):
    while True:
        try:
            with open(output, "a+") as f:
                resp = requests.get(source, stream=True, headers=headers, timeout=resp_timeout)
                for chunk in resp.iter_content(chunk_size):
                    with open(temp_mp3, "wb+") as g:
                        g.write(chunk)
                    convert(temp_mp3, temp_wav)
                    # f.write(transcribe(temp_wav))
                    print(transcribe(temp_wav))
                    
        except:
            print("Retrying...")
            time.sleep(5)
        

if __name__ == "__main__":
    main(source_url, output_file)



