# apg_flask
Flask wrapper around the [audio program generator](https://github.com/jeffwright13/audio_program_generator) module

# Current status
beta- (meaning, it runs locally on my Macbook Pro w/ Catalina 10.15.7,
 with ffmpeg version 4.4 installed via homebrew; and has been ported to
 digitalocean vps, ubuntu 18.04 LTS)

# Prerequisites
* Some relatively recent version of Python (3.7+)
* FFMPEG with at least the ability to read mp3s and wavs, and write mp3s

# Basic use
* clone the repo
* cd into it
* create a virtual environment
* pip install -r requirements.txt
* vi .env
* set your environment variables:
    * DEBUG=[True/False]
* flask run
* point browser at http://127.0.0.1:5000/
* fill out the form, submit, and wait for browser to serve up your freshly mixed mp3 file :-)


# Author:
Jeff Wright <jeff.washcloth@gmail.com>
