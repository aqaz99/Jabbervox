import re
from flask import Flask, render_template, url_for, jsonify, make_response, send_file, request
import json
import os # for executing shell commands
from make_conversation import *
app = Flask(__name__)

speakers_list = ["Hillary Clinton", "Barack Obama"]
# First flask route, landing page
conversation = {}
@app.route('/', methods=['GET','POST'])
def index():
    global conversation
    processed_text = ""
    speaker_choice = ""
    # Display text in page 
    if(request.method == "POST"):
        # Get speaker
        speaker = request.form.get('speaker_dropdown')
        speaker_choice = speaker
        if(speaker == "Hillary Clinton"):
            speaker = "HLCL"
        else:
            speaker = "BKOB"

        current_step = len(conversation)
        
        # Get first speaker text
        if("speaker" in request.form): # Did they provide text?
            first_speaker_text = request.form['speaker']

            if(first_speaker_text != ""):
                speaker_processed_text = "Text to generate:" + speaker + " - " + first_speaker_text.upper()
                conversation[f"{current_step}-{speaker}"] = first_speaker_text

        if("generate" in request.form and current_step > 0): # They want to generate the conversation
            make_conversation(conversation)
            conversation.clear()
            return send_file(f'./outputs/conversation/conversation.wav', download_name='conversation.wav', as_attachment=True)

        # Generate and return wav file to user # False is to not generate convo
        # os.system("bash ./scripts/generate_text.sh {} from_api \"{}\" false".format(speaker_one, first_speaker_text))
        # try:
        #     return send_file(f'./outputs/{speaker_one}/from_api.wav', download_name='from_api.wav', as_attachment=True)
        # except Exception as e:
        #     return str(e)
    return render_template('index.html', speakers=speakers_list, to_display=processed_text, conversation_full=conversation, speaker_choice=speaker_choice)


# Speakers
@app.route('/speakers')
def speakers():
    return render_template('speakers.html')

# Conversations
@app.route('/conversations')
def conversations():
    return render_template('conversations.html')

# How To
@app.route('/howto')
def howto():
    return render_template('howto.html')


# API base
@app.route('/api', methods=['GET'])
def api():
    # Load in local data
    with open('../wav_youtube/video_config.json') as file:
        data = json.load(file)
        print(data)

    headers = {"Content-Type": "application/json"}
    return make_response(data, 200, headers)


@app.route('/api/text_to_speech', methods=['GET'])
def textToSpeech():
    speaker = request.args.get('speaker')
    speaker = speaker.replace("\"","")

    if(not speaker):
        print("--- No speaker was given! ---")
        speaker = "HLCL"

    text = request.args.get('text')
    text = text.replace("\"","")
    print(text)
    if(not text):
        print("--- No text was given! ---")
        text = "Hello from default text!"
    
    # The user can input the text with spaces in the URL and it will still work, %20 will be automatically added for spaces
    os.system("bash ./scripts/generate_text.sh {} from_api \"{}\"".format(speaker, text))
    try:
        return send_file(f'./outputs/{speaker}/from_api.wav', download_name='from_api.wav')
    except Exception as e:
        return str(e)

@app.route('/api/pull', methods=['GET'])
def gitPull():
    os.system("git pull")
    headers = {"Content-Type": "application/json"}
    return make_response("Got changes",200, headers)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")

application = app