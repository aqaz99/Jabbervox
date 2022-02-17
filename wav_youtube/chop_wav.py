from __future__ import unicode_literals
import time
from pydub import AudioSegment
import youtube_dl

# This takes about the same time as the online converter
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192'
    }],
    'postprocessor_args': [
        '-ar', '16000'
    ],
    'prefer_ffmpeg': True,
    'keepvideo': False,
    'outtmpl': 'youtube_video'
}

# Downloading a 9.5 minute video takes aroun ~2 minutes
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['http://www.youtube.com/watch?v=B15Sd0QiVzw'])

# # Sleep for a few seconds to allow file to finalize
time.sleep(3)

# Examples of output from parsing transcript
# MCDM-1|his body is disintegrating he is not of this world and the strain of being here is killing him he is not like us he is Start: 0.0 Duration: 4.38
# MCDM-2|not one of us he can do amazing things he has one chance to return to his people if he can make it to the Start: 6.96 Duration: 5.4
# MCDM-3|rendezvous coordinates at the appointed time he will live he will leave us and return to the world he belongs him if he Start: 13.74 Duration: 4.14
# MCDM-4|fails he dies there are humans who care about him aid him but there are other humans chasing him they want to use him Start: 20.369 Duration: 5.49

t1 = 0.0 #Works in milliseconds
t2 = 6.96 * 1000
t3 = 13.74 * 1000
t4 = 20.369 * 1000 
newAudio = AudioSegment.from_wav("wav") # wav is filename here
# First - This is for testing
newAudio_temp = newAudio[t1:t2]
newAudio_temp.export('chopped1.wav', format="wav") #Exports to a wav file in the current path.
# Second
newAudio_temp = newAudio[t2:t3]
newAudio_temp.export('chopped2.wav', format="wav") #Exports to a wav file in the current path.
# Third
newAudio_temp = newAudio[t3:t4]
newAudio_temp.export('chopped3.wav', format="wav") #Exports to a wav file in the current path.
# # Fourth
# newAudio = newAudio[t1:t2]
# newAudio.export('chopped.wav', format="wav") #Exports to a wav file in the current path.