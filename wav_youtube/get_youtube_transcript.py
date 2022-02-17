from __future__ import unicode_literals

# Grab youtube video transcript with python
from youtube_transcript_api import YouTubeTranscriptApi

# Wav chop and wave download 
import time
from pydub import AudioSegment
import youtube_dl
import os
import shutil # For deleting directories that are not empty




## ----- Get And Parse Transcript -----##
print("Getting and Parsing Youtube Transcript Into Metadata File")
# Exaple of returned json 
#  {'text': "worried and desperate he hasn't given", 'start': 278.78, 'duration': 3.84}
youtube_video = "B15Sd0QiVzw"
csv_tag = "MCDM"

my_script = YouTubeTranscriptApi.get_transcript(youtube_video)
counter = 0
label = 0
time_stamps = []
to_write = []
script_len=len(my_script)


# print(script_len)
for index, item in enumerate(my_script):
    # Combine every other line of transcript to bring down count of individual wav files needed
    if(counter % 3 == 0):
        to_print = "{}-{}|{} {} {}".format(
            csv_tag,
            label, 
            my_script[counter]["text"], 
            (my_script[counter+1]["text"] if counter+1 < script_len else ""), # Ternary operators to not index past length of my_script
            (my_script[counter+2]["text"] if counter+2 < script_len else "")
        )
        to_write.append(to_print)
        label+=1
        time_stamps.append(item["start"])
        # print(to_print,"Start:", item["start"], "Duration:", item["duration"])
    counter+=1

# Write to text file EXAMPLE-001|Example text here
f = open("metadata.csv", "w")
for item in to_write:
    f.write(item)
    f.write('\n')
f.close()
print("Finished Creating Transcript and Metadata File")
## ----- Get And Parse Transcript -----##

# Delete Previous Audio Files if they exist
if os.path.exists("./wav"):
    os.remove("./wav")

if os.path.exists("./youtube_video.part"):
    os.remove("./youtube_video.part")


## ----- Download Youtube Audio As Wav -----##
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

# # Downloading a 9.5 minute video takes aroun ~2 minutes
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['http://www.youtube.com/watch?v=B15Sd0QiVzw'])
# ## ----- Download Youtube Audio As Wav -----##

# # # Sleep for a few seconds to allow file to finalize
time.sleep(3)

# Examples of output from parsing transcript
# MCDM-1|his body is disintegrating he is not of this world and the strain of being here is killing him he is not like us he is Start: 0.0 Duration: 4.38
# MCDM-2|not one of us he can do amazing things he has one chance to return to his people if he can make it to the Start: 6.96 Duration: 5.4
# MCDM-3|rendezvous coordinates at the appointed time he will live he will leave us and return to the world he belongs him if he Start: 13.74 Duration: 4.14
# MCDM-4|fails he dies there are humans who care about him aid him but there are other humans chasing him they want to use him Start: 20.369 Duration: 5.49


## ----- Chop Up Youtube Audio Into Small Wavs -----##
shutil.rmtree('./wavs', ignore_errors=True) # Delete if exists
# Create dir for wavs
os.mkdir('./wavs/')
original_audio = AudioSegment.from_wav("wav") # wav is filename here

len_timestamps = len(time_stamps)
for index, time in enumerate(time_stamps):

    t1 = time_stamps[index] * 1000
    if(index+1 >= len_timestamps): # Final file
        new_audio = original_audio[t1:]
        # Export chopped portion
        destination = './wavs/{}-{}.wav'.format(csv_tag, index)
        new_audio.export(destination, format="wav") #Exports to a wav file in the current path.
        break
    else:
        t2 = time_stamps[index+1] * 1000 # Account for milliseconds

    # Create new clip and chop it
    new_audio = original_audio[t1:t2]

    # Export chopped portion
    destination = './wavs/{}-{}.wav'.format(csv_tag, index)
    new_audio.export(destination, format="wav") #Exports to a wav file in the current path.
## ----- Chop Up Youtube Audio Into Small Wavs -----##