from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from pygame import mixer
import flask
from flask import request, render_template, send_from_directory
from flask_cors import CORS
import os
import sys
from pathlib import Path

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

input_device = sys.argv[1] if len(sys.argv) > 1 else "CABLE Input (VB-Audio Virtual Cable)"

mixer.init(devicename=input_device)

@app.route('/playSoundThroughMic', methods=["GET"])
def playSoundThroughMic():
	song_index = int(request.args.get("song_index"))
	files_list = os.listdir("sounds")
	for filename in files_list:
		if files_list.index(filename) == song_index:
			print(f"playing {filename}")
			mixer.music.load(f"sounds/{filename}")
			mixer.music.play()
	return "played"

@app.route("/")
def load_index():
	sounds = []
	for sound_file in os.listdir("sounds"):
		sound_dict = {}
		if sound_file.endswith(".wav"):
			sound_name = Path(sound_file).stem
			sound_dict["name"] = sound_name
			sound_dict["path"] = sound_file
			for thumbnail_file in os.listdir("thumbnails"):
				thumbnail_name = Path(thumbnail_file).stem
				if thumbnail_name == sound_name:
					sound_dict["thumbnail"] = thumbnail_file
			sounds.append(sound_dict)
			print(sounds)
	return render_template("index.html", sounds=sounds)

@app.route('/thumbnails/<path:thumbnail_name>')
def send_report(thumbnail_name):
    return send_from_directory('thumbnails', thumbnail_name)

@app.route('/playSound', methods=["GET"])
def playSound():
	sound_name = request.args.get("sound_name")
	if os.path.isfile(f"sounds/{sound_name}"):
		print(f"Playing {sound_name}")
		mixer.music.load(f"sounds/{sound_name}")
		mixer.music.play()
	return "played if file exists"

@app.route('/stopPlaying', methods=["GET"])
def stopPlaying():
	mixer.music.stop()
	return "stopped playing"

app.run(host='0.0.0.0', port=54000, debug=True)