import os
import celery
import raven


class TraderCelery(celery.Celery):

	def on_configure(self):
		pass


app = TraderCelery('trader')


app = config_from_object('django.conf.settings', namespace='CELERY')


app.autodiscover_tasks()