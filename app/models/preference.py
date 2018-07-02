from django.core.exceptions import ValidationError
from django.db import models


"""
Preference models
"""


class AlertnessInterval(models.Model):

    """
    Represents the interval at which alertness questionnaires
    should be displayed
    """

    interval = models.IntegerField(
        verbose_name='interval (in minutes)')  # the interval in minutes

    class Meta:
        verbose_name_plural = 'alertness questionnaire interval'

    def __str__(self):
        return str(self.interval)

    def single_instance(self, *args, **kwargs):
        """
        Ensures that only one instance is saved to the database.
        If the administrator tries to create a new interval when an interval
        already exists in the database, a validation error will be displayed.
        """
        if (AlertnessInterval.objects.count() > 0 and self.id != AlertnessInterval.objects.get().id):
            raise ValidationError('Please modify the existing alertness questionnaire interval.')

    def clean(self):
        self.single_instance(self)  # call the single instance check every time a value is prepared for db insertion
