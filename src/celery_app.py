from celery import Celery
from .settings import Config

celery_app = Celery(__name__)
celery_app.config_from_object(Config)
