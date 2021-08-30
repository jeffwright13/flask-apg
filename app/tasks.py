import logging
import os

from dotenv import load_dotenv

from app import app
from app.celery import make_celery
from app.aws import create_audio_mix as _create_audio_mix

load_dotenv()

app.config.update(
    CELERY_BROKER_URL=os.environ["CELERY_BROKER_URL"],
)
celery = make_celery(app)


@celery.task()
def create_audio_mix(*args, **kwargs):
    response = _create_audio_mix(*args, **kwargs)

    file = response.get("result_file")
    exception = response.get("exception")
    status_code = response.get("status_code")
    message = response.get("message")

    if status_code == 200:
        logging.debug(
            f"AWS generated mix file: {file}")
    # sometimes lambda returns something app developer did not define,
    # e.g. {'message': 'Endpoint request timed out'}
    elif message:
        logging.error(
            ("AWS failed to generate mix file, "
             f"message returned: {message}"))
    else:
        logging.error(
            ("AWS failed to generate mix file, "
             f"exception: {exception}"))

    # TODO insert into DB result table
