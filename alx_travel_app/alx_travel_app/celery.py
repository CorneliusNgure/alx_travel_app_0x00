import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_travel_app.settings")

app = Celery("alx_travel_app")

# Use Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodiscover tasks from installed apps
app.autodiscover_tasks()

# broker
# app.conf.broker_url = "amqp://kings:prenuptial@127.0.0.1:5672//"
# app.conf.result_backend = "rpc://"

