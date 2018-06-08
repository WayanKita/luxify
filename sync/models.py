from django.db import models
from django.utils import timezone

# Create your models here.
class Date(models.Model):
	date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.date)

