"""
Author:
    Jeff Wright <jeff.washcloth@gmail.com>
"""
import sys
import math
from pathlib import Path
from gtts import gTTS
from pydub import AudioSegment


class Apg:
    def __init__(self, phrase_file: str, to_mix: bool=False, sound_file: str="", attenuation: int=0):
        """Initialize class instance"""
        self.phrase_file = Path(phrase_file)  # Input file to generate speech segments
        self.speech_file = None  # Generated speech/silence
        self.mix_file = None  # Mixed speeech/sound
        self.to_mix = bool(to_mix)  # Specifies if mixing will take place
        self.sound_file = Path(sound_file)  # File with which to mix generated speech
        self.attenuation = int(attenuation)  # Attenuation value, if mixing
        self.save_file = str(Path(phrase_file).parent / Path(phrase_file).stem) + ".mp3"

    def gen_speech(self):
        """Generate a combined speech file, made up of gTTS-generated speech
        snippets from each line in the phrase_file + corresponding silence."""

        with open(self.phrase_file, "r") as f:
            combined = AudioSegment.empty()
            lines = f.readlines()
            num_rows = 0

            for line in lines:
                num_rows += 1

                try:
                    phrase, interval = line.split(";")
                except Exception as e:
                    print("Error parsing input file as CSV:")
                    print(line)
                    print(e.args)
                    sys.exit()

                if len(phrase) == 0:
                    print("Error: gTTS requires non-empty text to process.")
                    print("File: ", self.phrase_file)
                    print("Line number: ", num_rows)
                    sys.exit()

                # Each speech snippet generated from gTTS is saved locally
                # in a cache (if that exact phrase had not already been used).
                # Otherwise, it is simply re-used.
                Path.mkdir(Path.cwd() / ".cache") if not Path(
                    Path.cwd() / ".cache"
                ).exists() else None
                file = Path.cwd() / ".cache" / (phrase + ".mp3")
                if not Path(file).exists():
                    speech = gTTS(phrase)
                    speech.save(file)

                # Add the current speech snippet + corresponding silence
                # to the combined file, building up for each new line.
                speech = AudioSegment.from_file(file, format="mp3")
                combined += speech
                silence = AudioSegment.silent(duration=1000 * int(interval))
                combined += silence

        self.speech_file = combined

    def mix(self, segment1, segment2, seg2_atten=0, fadein=3000, fadeout=6000):
        """
        Mixes two pydub AudioSegments, then fades the result in/out.
        Returns mixed AudioSegment.
        """
        duration1 = len(segment1)
        duration2 = len(segment2)

        if duration1 > duration2:
            times = math.ceil(duration1 / duration2)
            segment2_normalized = segment2 * times
            segment2_normalized = segment2_normalized[:duration1]
        else:
            segment2_normalized = segment2[:duration1]

        return (segment1).overlay(
            (segment2_normalized - float(seg2_atten)).fade_in(fadein).fade_out(fadeout)
        )
