# Grab youtube video transcript with python
from youtube_transcript_api import YouTubeTranscriptApi

# Exaple of returned json 
#  {'text': "worried and desperate he hasn't given", 'start': 278.78, 'duration': 3.84}
my_script = YouTubeTranscriptApi.get_transcript("B15Sd0QiVzw")
counter = 0
label = 0

script_len=len(my_script)
# print(script_len)
for index, item in enumerate(my_script):
    # Combine every other line of transcript to bring down count of individual wav files needed
    if(counter % 3 == 0):
        label+=1
        to_print = "MDCM-{}|{} {} {}".format(
            label, 
            my_script[counter]["text"], 
            (my_script[counter+1]["text"] if counter+1 < script_len else ""), # Ternary operators to not index past length of my_script
            (my_script[counter+2]["text"] if counter+2 < script_len else "")
            )
        print(to_print,"Start:", item["start"], "Duration:", item["duration"])
    counter+=1