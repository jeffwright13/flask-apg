# apg_flask
Flask wrapper around the [audio program generator](https://github.com/jeffwright13/audio_program_generator) module

# Current status
alpha+ (meaning, it runs locally on my Macbook Pro w/ Catalina 10.15.7,
 with ffmpeg version 4.4 installed via homebrew)

# Prerequisites
* Some relatively recent version of Python (3.7+)
* FFMPEG with at least the ability to read mp3s and wavs, and write mp3s

# Basic use
* clone the repo
* cd into it
* create a virtual environment
* pip install -r requirements.txt
* export APG_FILE_FOLDER=<path_to_local_dick_to_store_files>
* export FLASK_APP=app
* export FLASK_ENV=development
* flask run
* point browser at http://127.0.0.1:5000/setvals
* fill out the form, submit, and wait for browser to serve up your freshly mixed mp3 file :-)

# Author:
Jeff Wright <jeff.washcloth@gmail.com>
