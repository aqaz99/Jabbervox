import re
from flask import Flask, render_template, url_for, jsonify, make_response, send_file, request
import json
import os # for executing shell commands
app = Flask(__name__)

speakers_list = ["Matt Colville", "Hillary Clinton", "Barack Obama"]
# First flask route, landing page
@app.route('/', methods=['GET','POST'])
def index():
    processed_text = ""
    # Display text in page 
    if(request.method == "POST"):
        text = request.form['text']
        speaker = request.form.get('speaker_dropdown')
        processed_text = "Text to generate:" + speaker + " - " + text.upper()
        print(processed_text)

        if(speaker == speakers_list[1]):
            speaker = "HLCL"
        else:
            speaker = "BKOB"
        # Generate and return wav file to user # False is to not generate convo
        os.system("bash ./scripts/generate_text.sh {} from_api \"{}\" false".format(speaker, text))
        try:
            return send_file(f'./outputs/{speaker}/from_api.wav', download_name='from_api.wav', as_attachment=True)
        except Exception as e:
            return str(e)
    return render_template('index.html', speakers=speakers_list, to_display=processed_text)


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