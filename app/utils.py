import os
from base64 import b64encode, b64decode

import boto3
from werkzeug.datastructures import FileStorage

FILE_URL = 'https://{bucket}.s3.us-east-2.amazonaws.com/{filename}'
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")


def upload_to_s3(file: FileStorage, bucket=AWS_S3_BUCKET) -> str:
    """Upload a file object to S3 returning its public URL

    Super helpfuL: https://stackoverflow.com/a/60239208
    """
    s3_resource = boto3.resource(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    bucket = s3_resource.Bucket(bucket)

    filename = file.filename
    bucket.Object(filename).put(Body=file.read(),
                                ACL='public-read')

    return FILE_URL.format(bucket=bucket.name,
                           filename=filename)


def encode_mp3_file(mp3_file):
    with open(mp3_file, 'rb') as f:
        return b64encode(f.read()).decode('utf-8')


def decode_mp3_file(encoded_file, outfile="out.mp3"):
    with open(outfile, 'wb') as f:
        f.write(b64decode(encoded_file))
    return outfile
