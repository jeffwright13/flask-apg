import os

import boto3
from werkzeug.datastructures import FileStorage
import requests

FILE_URL = 'https://{bucket}.s3.us-east-2.amazonaws.com/{filename}'
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
AWS_GATEWAY_URL = os.getenv("AWS_GATEWAY_URL")


def _upload_to_s3(file: FileStorage, bucket=AWS_S3_BUCKET) -> str:
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


def create_audio_mix(req_phrase_file_obj,
                     req_sound_file_obj,
                     to_mix,
                     attenuation):
    """Upload files to S3 and invoke apg in AWS Lambda

    TODO: have the lambda function store the result file in
    the same or a different S3 bucket, then check this
    cache here first for quick retrieval
    """
    phrase_file_s3_path = _upload_to_s3(req_phrase_file_obj)
    sound_file_s3_path = _upload_to_s3(req_sound_file_obj)

    payload = dict(
        phrase_file=phrase_file_s3_path,
        sound_file=sound_file_s3_path,
        to_mix=to_mix,
        attenuation=attenuation)

    resp = requests.post(AWS_GATEWAY_URL, json=payload)
    return resp.json()
