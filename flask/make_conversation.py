from pydub import AudioSegment
from pydub.playback import play
import re
import os

# We are going to trim all audio files above 16 seconds
# Need to sort filenames when creating csv file
def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)] 
    return sorted(l, key=alphanum_key)

# Format is speaker-when to say line

def make_conversation(conversation):
    print("Convo:",conversation)
    destination = './outputs/conversation'
    os.system(f"rm {destination}/conversation.wav")
    # os.system("bash ./scripts/generate_text.sh {} from_api \"{}\"".format(speaker, text))
    for item in conversation:
        file_name = item
        speaker = item.split('-')[1]
        text = conversation[item]
        os.system("bash ./scripts/generate_text.sh {} {} \"{}\" true".format(speaker, file_name, text))

    # Prepend small silence for conversation, also gives us starting point to append to
    full_conversation_audio = AudioSegment.silent(duration=150)
    silence_chunk = AudioSegment.silent(duration=200)

    # pydub append adds 100ms crossfade
    for audio_file in natural_sort(os.listdir(destination)):
        conversation_piece = AudioSegment.from_file(destination + '/' + audio_file)

        full_conversation_audio = full_conversation_audio + silence_chunk + conversation_piece

    full_conversation_audio.export(destination + '/conversation.wav', format="wav")

    for audio_file in natural_sort(os.listdir(destination)):
        if(audio_file != 'conversation.wav'):
            os.system(f"rm {destination}/{audio_file}")