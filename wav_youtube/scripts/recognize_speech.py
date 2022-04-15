# Speech recognizer python test
# Links https://realpython.com/python-speech-recognition/
# Also may want to check out aubio
# https://stackoverflow.com/questions/40896370/detecting-the-index-of-silence-from-a-given-audio-file-using-python

# Helpful commands for doing wav conversion
# 


# Steps to convert aax to wav file
# 1. Get key https://audible-converter.ml/
# 2. ffmpeg -activation_bytes b5b70d07 -i WhatHappenedPart1_ep5.aax test2.wav -ac 1 #-ar 22050 # -ar is bitrate but it didn't make the file smaller
#
#
from locale import normalize
from math import floor
from typing import Counter
from unicodedata import name
from pydub import AudioSegment, silence
import speech_recognition as sr
from helpers import *
from pydub.silence import split_on_silence

r = sr.Recognizer() 


# ----- Enter Custom Speaker Config Here! ----- #
speaker_id = "LAFB"

# ----- Create speaker directory ----- #
directory = '../../training_data/{}'.format(speaker_id)

if not os.path.exists(directory): # Need to mkdir for wavs
    # Create dir for wavs
    os.mkdir(directory)
    os.mkdir(directory+"/wavs") # Make wavs dir too


speaker_audio = AudioSegment.from_wav("/home/aqaz/Downloads/laurence.wav")


name_counter = int(get_most_recent_metadata_line(speaker_id))
print("Total minutes in audio:",speaker_audio.duration_seconds/60)


# # t1 can also be the first cutoff point
# t1 = 13 * 1000 # Beginning audio slice
# t2 = 60 * 1000 # Ending audio slice

# # Chop up big wav into smaller, minute long wavs
# wavs = []
# chunks = []
# for i in range(floor(speaker_audio.duration_seconds/60)): # floor(speaker_audio.duration_seconds/60)
#     print("Processing at", i)
#     # Last chunk
#     if(i >= speaker_audio.duration_seconds):
#         split_audio = split_on_silence(speaker_audio[t1:], min_silence_len=650, silence_thresh=-66)
#         break

#     split_audio = split_on_silence(speaker_audio[t1:t2], min_silence_len=650, silence_thresh=-66)

#     # Don't add empty files or too short audio to chunks
#     if(split_audio):
#         for item in split_audio:
#             if(item.duration_seconds != 0):
#                 chunks.append(item)
#     t1 = t2
#     t2 = 60 * (i+1) * 1000

# print("Done processing file")

# print("Got",len(chunks),"total chunks")



# # ----- Export Chopped Audio Files ----- #
# silence_chunk = AudioSegment.silent(duration=200)
# appended = False
# # Get most recent meta data line for counter

# # Export chopped audio to file, if audio is too short, append to another
# for index, chunk in enumerate(chunks):
#     if(appended): # If we appended this audio clip to the previous, skip it
#         appended = False
#         continue
#     file_name = "{}/wavs/{}-{}.wav".format(directory, speaker_id,name_counter, iter)
#     name_counter += 1
#     if(chunk.duration_seconds < 2.5 and index < len(chunks)-1):
#         # print("Appending two wavs {} + {}".format(chunk.duration_seconds, chunks[index+1].duration_seconds))
#         appended_audio = chunk + silence_chunk + chunks[index+1]
#         appended_audio.export(file_name, format="wav") 
#         appended = True
#         continue

#     # print("silencing ", file_name, " Length = ", chunk.duration_seconds)
#     chunk.export(file_name, format="wav") 


# print("Creating metadata.csv")
# # assign directory

# time.sleep(60)
# iterate over files in
# that directory
for filename in natural_sort(os.listdir(directory+'/wavs')):
    get_last_file_num = int(filename.split("-")[1].split(".")[0])
    if(get_last_file_num <= name_counter):
        continue

    f = os.path.join(directory+'/wavs', filename)
    # checking if it is a file
    if os.path.isfile(f):
        # print("Analyzing ", f)

        audiofile_to_recognize = sr.AudioFile(f)
        with audiofile_to_recognize as source:
            recognized = r.record(source)

        recognized_speech = r.recognize_google(recognized)


        # Write to text file EXAMPLE-001|Example text here
        f = open("../../training_data/{}/metadata.csv".format(speaker_id), "a")
        f.write("{}||{}\n".format(filename.split('.')[0], recognized_speech))

print("Finished Creating Transcript and Metadata File")
# f.close()