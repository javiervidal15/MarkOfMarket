from __future__ import absolute_import
from celery import shared_task
import appmark


@shared_task
def guardarRegistros():
    appmark.views.guardarRegistros()