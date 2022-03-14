import speech_recognition as sr
import re
import os
r = sr.Recognizer()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="jabbervox-4f38518a0c72.json"


# Need to sort filenames when creating csv file
def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)] 
    return sorted(l, key=alphanum_key)

speaker_id = 'BKOB'
directory = '../../training_data/{}'.format(speaker_id)

counter = 0
for filename in natural_sort(os.listdir(directory+'/wavs')):
    counter += 1
    if(counter > 25):
        break
    f = os.path.join(directory+'/wavs', filename)
    # checking if it is a file
    if os.path.isfile(f):
        # print("Analyzing ", f)

        audiofile_to_recognize = sr.AudioFile(f)
        with audiofile_to_recognize as source:
            recognized = r.record(source)

        recognize_list = []

        recognize_list.append(r.recognize_google(recognized))
        # recognize_list.append(r.recognize_bing(recognized))
        recognize_list.append(r.recognize_google_cloud(recognized))
        # recognize_list.append(r.recognize_houndify(recognized))
        # recognize_list.append(r.recognize_ibm(recognized))
        # recognize_list.append(r.recognize_sphinx(recognized))
        # recognize_list.append(r.recognize_wit(recognized))

        for item in recognize_list:
            print(item)