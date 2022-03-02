# Speech recognizer python test
import speech_recognition as sr
r = sr.Recognizer() 
audio_file = sr.AudioFile('./wavs/MCDM-0.wav')

with audio_file as source:
    recognized = r.record(source)

print(r.recognize_google(recognized))

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
