# Speech recognizer python test
# Links https://realpython.com/python-speech-recognition/
# Also may want to check out aubio
# https://stackoverflow.com/questions/40896370/detecting-the-index-of-silence-from-a-given-audio-file-using-python
from pydub import AudioSegment, silence
import speech_recognition as sr
r = sr.Recognizer() 
audio_file = sr.AudioFile('testing.wav')

with audio_file as source:
    recognized = r.record(source)

print(r.recognize_google(recognized))

myaudio = AudioSegment.from_wav('testing.wav')

silence = silence.detect_silence(myaudio, min_silence_len=400, silence_thresh = -18)
silence = [((start/1000),(stop/1000)) for start,stop in silence] #convert to sec

print(silence)

"""
Capturing Segments With offset and duration
What if you only want to capture a portion of the speech in a file? The record() method accepts a duration keyword argument that stops the recording after a specified number of seconds.

For example, the following captures any speech in the first four seconds of the file:

>>> with harvard as source:
...     audio = r.record(source, duration=4)
...
>>> r.recognize_google(audio)
'the stale smell of old beer lingers'

"""
