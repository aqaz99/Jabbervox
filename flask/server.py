from flask import Flask, render_template, url_for, jsonify, make_response
import json
app = Flask(__name__)


# First flask route, landing page
@app.route('/')
def index():
    return render_template('index.html')

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


@app.route('/api/text_to_speech/<text>', methods=['GET'])
def textToSpeech(text):
    return make_response(text)


if __name__ == '__main__':
    app.run(debug=True)