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
# So bkob-1 would go, then hlcl-2 would be after. A speaker could have multiple lines such as bkob-1, bkob-2 and they would speak in order
convo = {'1-BKOB': "Greetings to you Hillary, how are you today?", 
         '2-HLCL': "Hi Barack, today is going quite well for me. How are you?",
         "3-BKOB": "Things are going good on my end too, thanks for asking."
        }

# os.system("bash ./scripts/generate_text.sh {} from_api \"{}\"".format(speaker, text))
for item in convo:
    file_name = item
    speaker = item.split('-')[1]
    text = convo[item]
    os.system("bash ./scripts/generate_text.sh {} {} \"{}\" true".format(speaker, file_name, text))


destination = './outputs/conversation'
# Prepend small silence for convo, also gives us starting point to append to
full_conversation_audio = AudioSegment.silent(duration=150)
silence_chunk = AudioSegment.silent(duration=200)


# pydub append adds 100ms crossfade
for audio_file in natural_sort(os.listdir(destination)):
    conversation_piece = AudioSegment.from_file(destination + '/' + audio_file)

    full_conversation_audio = full_conversation_audio + silence_chunk + conversation_piece

play(conversation_piece)
full_conversation_audio.export(destination + '/conversation.wav', format="wav")