from .celery import app
from celery import shared_task
from django.core.files.storage import default_storage

from main.utils.mail.emailer import ClientEmailer


@app.task
def send_order(order):
    emailer = ClientEmailer()
    emailer.send_order( order )
