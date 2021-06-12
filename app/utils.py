from base64 import b64encode, b64decode


def encode_mp3_file(mp3_file):
    with open(mp3_file, 'rb') as f:
        return b64encode(f.read()).decode('utf-8')


def decode_mp3_file(encoded_file, outfile="out.mp3"):
    with open(outfile, 'wb') as f:
        f.write(b64decode(encoded_file))
    return outfile
