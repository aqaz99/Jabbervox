#helper functions
import shutil # For deleting directories that are not empty\
import os
import time as tm
import re
from pydub import AudioSegment

# Need to sort filenames when creating csv file
def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)] 
    return sorted(l, key=alphanum_key)

def start_fresh():
    # Delete metadata csv
    if os.path.exists("./metadata.csv"):
        os.remove("./metadata.csv")
    else:
        f = open("metadata.csv", "w")
        f.close()

    shutil.rmtree('./wavs', ignore_errors=True) # Delete if exists


# Get the number of the most recent line in the metadata file so we can append to it for new additions
def get_most_recent_metadata_line(speaker_id):
    meta_loc = "../../training_data/{}/metadata.csv".format(speaker_id)
    if not os.path.exists(meta_loc): # Need to mkdir for wavs
        # Create dir for wavs
        os.system("touch {}".format(meta_loc))

    metafile = open("../../training_data/{}/metadata.csv".format(speaker_id), "r")
    last_line = 0
    for item in metafile:
        last_line = item
    if(last_line == 0):
        print("Metadata file empty")
        return last_line
    # When the loop gets here we will have the last line text, inefficient but it works
    # EXMPL-001||Hello World! -> split | -> ['EXMPL-001', 'Hello World!'] -> 'EXMPL-001'.split('-')[1] = 001
    last_line = last_line.split('|')[0].split('-')
    return last_line[1]



def get_total_audio_length():
    pass

def run_training(run=False):
    if(run == True):
        print("-"*20)
        print("Will start training a new model in 15 seconds")
        tm.sleep(15)
        os.system("time CUDA_VISIBLE_DEVICES=0 python /home/aqaz/Desktop/TTS/recipes/ljspeech/glow_tts/train_glowtts.py")

# def convertToSingleChannel(directory):
#     for filename in natural_sort(os.listdir(directory+'/wavs')):
#         sound = AudioSegment.from_wav("/path/to/file.wav")
#         sound = sound.set_channels(1)
#         sound.export("/output/path.wav", format="wav")