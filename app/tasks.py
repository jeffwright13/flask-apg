import os

from dotenv import load_dotenv

from app import app
from app.celery import make_celery

load_dotenv()

app.config.update(
    CELERY_BROKER_URL=os.environ["CELERY_BROKER_URL"],
)
celery = make_celery(app)


@celery.task()
def add_together(a, b):
    return a + b
