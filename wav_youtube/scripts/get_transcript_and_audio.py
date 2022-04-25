from __future__ import unicode_literals

# Grab youtube video transcript with python
from youtube_transcript_api import YouTubeTranscriptApi

# Wav chop and wave download 
import time as tm
from pydub import AudioSegment
import youtube_dl
import os
import json

import datetime # for converting seconds into hrs:mins:scnds
# Helper functions
from helpers import *

## ----- Train after import? ----- ##
# print("NOTE: Don't run this script in VSCode's integrated terminal.")
# train_after = input("Would you like to train a new model after this script finishes? (yes) or (any other char)")
# if(train_after == "yes"):
#     print("Training will proceed afterwards")
#     train_after=True
# else:
#     print("No model will be trained after")
#     train_after=False
train_after=False
## ----- Get And Parse Transcript ----- ##
print("Getting and Parsing Youtube Transcript Into Metadata File")
speaker_id = "NDGTYT"
last_line = get_most_recent_metadata_line(speaker_id)

# Exaple of returned json 
#  {'text': "worried and desperate he hasn't given", 'start': 278.78, 'duration': 3.84}
with open("../video_config.json") as file:
    data = json.load(file)

if(last_line == ""):
    # Need counter outside of loop for continued
    transcript_label = 0
    video_label = 0
else:
    transcript_label = int(last_line) + 1
    video_label = int(last_line) + 1

total_audio_length = 0

if not os.path.exists("./wavs/"): # Need to mkdir for wavs
    # Create dir for wavs
    os.mkdir('./wavs/')

for item in data["videos"]:
    # Get the script for the video
    my_script = YouTubeTranscriptApi.get_transcript(item["id"])
    tm.sleep(.7) # Micro sleep to not overload api calls to transcript api
    # Go to the last entry of the transcript. The start + the duration will tell us how long the video is
    total_audio_length += my_script[len(my_script)-1]["start"]
    total_audio_length += my_script[len(my_script)-1]["duration"]
    if(item["complete"] == "true"):
        print("Skipping {}".format(item["id"]))
        continue
    print("Processing {}".format(item["id"]))
    csv_tag = item["speaker"]
    youtube_video = item["id"]#

    # my_script = YouTubeTranscriptApi.get_transcript(youtube_video)
    counter = 0
    time_stamps = []
    to_write = []
    script_len=len(my_script)

    # add complete to video_config.json so we don't repeat pulling video in future

    # print(script_len)
    for index, item in enumerate(my_script):
        # Combine every other line of transcript to bring down count of individual wav files needed
        if(counter % 3 == 0): # Set to 3 to keep batch size from overflowing memory
            to_print = "{}-{}||{} {} {}".format(
                csv_tag,
                transcript_label, 
                my_script[counter]["text"], 
                (my_script[counter+1]["text"] if counter+1 < script_len else ""), # Ternary operators to not index past length of my_script
                (my_script[counter+2]["text"] if counter+2 < script_len else "")
            ).replace('\n', ' ')
            # print("To print [{}]".format(to_print.replace('\n', '')))
            to_write.append(to_print)
            transcript_label+=1
            time_stamps.append(item["start"])
            # print(to_print,"Start:", item["start"], "Duration:", item["duration"])
        counter+=1

    # Write to text file EXAMPLE-001|Example text here
    f = open("metadata.csv", "a")
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
            '-ar', '20000' # Adjusted for training / Changed to 20000 for lower file size
        ],
        'prefer_ffmpeg': True,
        'keepvideo': False,
        'outtmpl': 'youtube_video'
    }

# I WILL NEED TO ACCOUNT FOR STUFF IN * * ASTERISKS
# MATT COLVILE HAS A VIDEO WHERE HE SHOWS A CLIP THAT ISN;T HIS VOICE

    # # # Downloading a 9.5 minute video takes aroun ~2 minutes
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['http://www.youtube.com/watch?v={}'.format(youtube_video)])
    except:
        print("Error getting {}, skipping to next video", youtube_video)
    # # ## ----- Download Youtube Audio As Wav -----##

    # # # # Sleep for a few seconds to allow file to finalize
    tm.sleep(1.1) # tm because of time variable overwrite

    # Examples of output from parsing transcript
    # MCDM-1|his body is disintegrating he is not of this world and the strain of being here is killing him he is not like us he is Start: 0.0 Duration: 4.38
    # MCDM-2|not one of us he can do amazing things he has one chance to return to his people if he can make it to the Start: 6.96 Duration: 5.4
    # MCDM-3|rendezvous coordinates at the appointed time he will live he will leave us and return to the world he belongs him if he Start: 13.74 Duration: 4.14
    # MCDM-4|fails he dies there are humans who care about him aid him but there are other humans chasing him they want to use him Start: 20.369 Duration: 5.49


    ## ----- Chop Up Youtube Audio Into Small Wavs -----##
    original_audio = AudioSegment.from_wav("wav") # wav is filename here

    len_timestamps = len(time_stamps)
    for index, time in enumerate(time_stamps):

        t1 = time_stamps[index] * 1000
        if(index+1 >= len_timestamps): # Final file
            new_audio = original_audio[t1:]
            # Export chopped portion
            destination = './wavs/stereo_{}-{}.wav'.format(csv_tag, video_label)
            video_label += 1
            new_audio.export(destination, format="wav") #Exports to a wav file in the current path.
            break
        else:
            t2 = time_stamps[index+1] * 1000 # Account for milliseconds

        # Create new clip and chop it
        new_audio = original_audio[t1:t2]

        # Export chopped portion
        destination = './wavs/stereo_{}-{}.wav'.format(csv_tag, video_label)
        video_label += 1
        new_audio.export(destination, format="wav") #Exports to a wav file in the current path.
    ## ----- Chop Up Youtube Audio Into Small Wavs ----- ##


# Run single channel conversion after all files are created
## ----- Convert Wav Files To Mono Channel ----- ##
print("Converting audio to single channel")
for file in os.listdir('./wavs'):
    if(file.find("stereo") == -1): # Skip wav files that have already been converted to single channel
        # print("Skipping ", file)
        continue

    new_name = file.split("_")[1] # Convert from stereo_EXMPL-001.wav -> EXMPL-001.wav
    os.system("ffmpeg -hide_banner -loglevel error -i './wavs/{}' -ac 1 './wavs/{}'".format(file, new_name))
    os.system("rm ./wavs/{}".format(file))

# for index, i in enumerate(time_stamps):
#     name = "{}-{}".format(csv_tag, video_label+index)
#     os.system("ffmpeg -hide_banner -loglevel error -i './wavs/stereo_{}.wav' -ac 1 './wavs/{}.wav'".format(name, name))
#     os.system("rm ./wavs/stereo_{}.wav".format(name))

print("Completed converting audio to single channel. Any errors would have been reported before this message")
if os.path.exists("./wav"): # Need to mkdir for wavs
    # Create dir for wavs
    os.system("rm wav")

print("-"*10,"\nTotal audio length of wav files: {}".format(str(datetime.timedelta(seconds=total_audio_length))))

run_training(train_after)
# I need to solve how to add more wav files dynamically using the count