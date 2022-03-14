# Helper file to check length of files in dataset, to help trim ones that are too long
from pydub import AudioSegment
import re
import os

# We are going to trim all audio files above 16 seconds
# Need to sort filenames when creating csv file
def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)] 
    return sorted(l, key=alphanum_key)


directory = '/home/aqaz/Desktop/Jabbervox/training_data/BKOB'

count = 0
to_trim = []
for filename in natural_sort(os.listdir(directory+'/wavs')):
    full_file_name = directory+'/wavs/'+filename
    audio_file = AudioSegment.from_wav(full_file_name)

    if(audio_file.duration_seconds > 16):
        count += 1
        # print(filename, "seconds:",audio_file.duration_seconds)
        to_trim.append(filename.split('.')[0])
        print("Removing file:",filename)
        os.system('rm {}'.format(full_file_name))

with open('/home/aqaz/Desktop/Jabbervox/training_data/BKOB/metadata.csv') as f:
    data = f.readlines()

for index, line in enumerate(data):
    for offender in to_trim:
        if(line.split('|')[0] == offender):
            print("Removing line {} from file".format(index))
            data[index] = ""

with open('/home/aqaz/Desktop/Jabbervox/training_data/BKOB/metadata.csv', 'w', encoding='utf-8') as file:
    file.writelines(data)
            
print("Total above 16 seconds:",count)