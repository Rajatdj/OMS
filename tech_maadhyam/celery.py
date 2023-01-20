# from __future__ import absolute_import
# import os
# from celery import Celery
# from django.conf import settings


# os.environ.setdefault('DJANGO_SETTINGS_MODULE','tech_maadhyam.settings')
# app = Celery('tech_maadhyam,')
# app.config_from_object('django.conf:settings')


# app.conf.beat_schedule = {
#         'Send_mail_to_Client': {
#             'task': 'send_email',
#             'schedule': 30, 
#         },
#         'second_scheduled_task': {
#             'task': 'new_task',
#             'schedule': 30, 
#         }
# }

# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
