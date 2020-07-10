import os
import sys
import random
import string
from pathlib import Path
from threading import Thread
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename

sys.path.append('./lab')
from encode import encode
from decode import decode

# Define the folders where we will perform steganography.
UPLOAD_FOLDER_ENCODE = os.path.abspath('./uploads/encode')
UPLOAD_FOLDER_DECODE = os.path.abspath('./uploads/decode')

# Create the folders if they do not exist.
Path(UPLOAD_FOLDER_ENCODE).mkdir(parents=True, exist_ok=True)
Path(UPLOAD_FOLDER_DECODE).mkdir(parents=True, exist_ok=True)

# Only these extensions are allowed to be uploaded.
ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', 'jpe', '.png']

# Create the app.
app = Flask(__name__)
app.config['UPLOAD_FOLDER_ENCODE'] = UPLOAD_FOLDER_ENCODE
app.config['UPLOAD_FOLDER_DECODE'] = UPLOAD_FOLDER_DECODE
socketio = SocketIO(app)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/encode', methods=['GET', 'POST'])
def encode():
	if request.method == 'POST':

		# Check that the POST request includes a file.
		try:
			if not 'file' in request.files:
				print('ERROR: no image file has been provided')
				return redirect(request.url)
		except Exception as exception:
			print(exception)
			return redirect(request.url)
		print('An image file has been provided')
		image = request.files['file']

		# Check that the image filename is valid.
		if image.filename == '':
			print('ERROR: image filename is not valid')
			return redirect(request.url)
		else:
			print('The image filename is valid')
		
		# Check the extension of the image.
		partialImageFilename = secure_filename(image.filename)
		fileExtension = os.path.splitext(partialImageFilename)[1]
		if fileExtension not in ALLOWED_EXTENSIONS:
			print('ERROR: the image provided does not have a valid extension')
			return redirect(request.url)
		else:
			print('The image has a valid extension')
		
		# Check that the POST request includes a message.
		if 'message' not in request.form:
			print('ERROR: no message has been provided')
			return redirect(request.url)
		else:
			message = request.form['message']
		
		# Store the image and the message inside the uploads folder.
		randomId = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
		finalImageFilename = os.path.join(app.config['UPLOAD_FOLDER_ENCODE'], randomId + partialImageFilename)
		image.save(finalImageFilename)
		finalMsgFilename = os.path.join(app.config['UPLOAD_FOLDER_ENCODE'], randomId + 'message.txt')
		with open(finalMsgFilename, 'w') as file:
			file.write(message)
		
		# Decide a name for the encoded image.
		Thread(target=encode, args=(finalImageFilename, finalMsgFilename)).start()
		
		return redirect(url_for('viewUploadedFile', filename='encoded.png'))
	
	else:
		return render_template('encode.html')

@app.route('/decode')
def decode():
	return render_template('decode.html')

@app.route('/uploads/<filename>')
def viewUploadedFile(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER_ENCODE'], filename)

@app.route('/about')
def about():
	return render_template('about.html')

if __name__ == '__main__':
	app.debug = True
	socketio.run(app, host='0.0.0.0', port=8080)
