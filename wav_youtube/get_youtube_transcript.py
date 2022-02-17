# Grab youtube video transcript with python
from youtube_transcript_api import YouTubeTranscriptApi

# Exaple of returned json 
#  {'text': "worried and desperate he hasn't given", 'start': 278.78, 'duration': 3.84}
my_script = YouTubeTranscriptApi.get_transcript("B15Sd0QiVzw")
index = 0
for item in my_script:
    to_print = "MDCM-{}|{}".format(index, item["text"])
    print(to_print, item["start"])
    index += 1