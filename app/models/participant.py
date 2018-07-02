from django.contrib.auth.models import User
from django.utils import timezone
from app.models.room import Desk, Room
from app.models.questionnaire import Choice
from django.db import models
from random import randint


"""
Participant models
"""


class Profile(models.Model):

    """
    Represents a research participant's user profile.
    This profile is determined based on the answers given in
    the demographic questionnaire.
    """

    answer = models.OneToOneField(
        Choice, on_delete=models.CASCADE)  # the questionnaire answer associated with this profile
    formula = models.CharField(
        max_length=300, default="100000")  # the formula used when recommending an illuminance value

    def __str__(self):
        return 'Answer ' + str(self.answer) + ' has formula: ' + self.formula


class Category(models.Model):

    """
    Represents a research participant's user category.
    This category is assigned randomly and determines the sections
    the participant can view in the mobile app.
    """

    name = models.CharField(max_length=250, unique=True)  # the name of the category
    visualization = models.BooleanField(default=True)  # whether visualization is enabled for this category
    recommendation = models.BooleanField(default=True)  # whether recommendation is enabled for this category
    guidance = models.BooleanField(default=True)  # whether guidance is enabled for this category

    class Meta:
        verbose_name_plural = 'categories'
        unique_together = ('visualization', 'recommendation', 'guidance')  # no categories should have the same layout

    def __str__(self):
        return self.name

    def random_category():

        """
        Generates a random user category
        """

        number_of_categories = Category.objects.count()
        random_category = Category.objects.all()[randint(0, number_of_categories - 1)]
        return random_category


class Participant(models.Model):

    """
    Represents a research participant
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # general user information
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='category_participant', blank=True, null=True)  # the participant's user category
    profile = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        related_name='profile_participant', blank=True, null=True)  # the participant's user profile
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        related_name='room_participant', blank=True, null=True)  # the room the participant is working in
    desk = models.ForeignKey(
        Desk,
        on_delete=models.SET_NULL,
        related_name='desk_participant', blank=True, null=True)  # the desk the participant is working at
    name = models.CharField(max_length=100, blank=True, null=True, default=None)  # the participant's name
    working = models.BooleanField(default=False)  # whether the participant has indicated that they are working
    questionnaire_done = models.BooleanField(
        default=False)  # whether the participant has completed the demographic questionnaire

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):

        """
        Assigns the participant to a random category
        """

        if not self.pk:
            self.category = Category.random_category()  # assign a random category
        super(Participant, self).save(*args, **kwargs)  # call the default save method

    def recommended_illuminance(self):

        """
        Returns the recommended illuminance level for this user
        """

        if self.profile is None:
            return 100000  # recommend the highest illuminance level
        else:
            formula = self.profile.formula
            return eval(formula)  # return the recommended illuminance level


class QuestionnaireAnswer(models.Model):

    """
    Represents a participant's questionnaire answer
    """

    participant = models.OneToOneField(
        Participant,
        on_delete=models.CASCADE,
        related_name='participant_questionnaire')  # the participant associated with this answer
    answer = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        related_name='choice_answer')  # the answer the participant has selected
    timestamp = models.DateTimeField(default=timezone.now, blank=True)  # the timestamp at which the answer was sent

    def __str__(self):
        return str(self.participant) + ' answered ' + str(self.answer)

    def save(self, *args, **kwargs):

        """
        Assigns the participant to the user profile associated with the participant's answer
        """

        self.participant.profile = Profile.objects.get(
            answer=self.answer)  # the profile associated with the participant's answer
        self.participant.save()  # save the modified participant object
        super(QuestionnaireAnswer, self).save(*args, **kwargs)  # call the default save method


class AlertnessQuestionnaireAnswer(models.Model):

    """
    Represents a participant's alertness questionnaire answer
    """

    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name='participant_alertness_questionnaire')  # the participant associated with this answer
    answer = models.IntegerField()  # the answer the participant has selected
    illuminance = models.FloatField(blank=True, null=True)  # the illuminance value at the participant's desk
    timestamp = models.DateTimeField(default=timezone.now, blank=True, null=True)  # the timestamp at which the answer was sent

    def __str__(self):
        return str(self.participant) + ' answered ' + str(self.answer) + ' (' + str(self.illuminance) + ')'

    def save(self, *args, **kwargs):

        """
        Sets the illuminance level
        """

        if self.participant.desk:
            self.illuminance = Desk.objects.get(id=self.participant.desk.id).illuminance
        super(AlertnessQuestionnaireAnswer, self).save(*args, **kwargs)  # call the default save method


class Analytics(models.Model):

    """
    Represents actions the participant has taken in the mobile application
    """

    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE, related_name='participant_analytics')  # the participant associated with this event
    event = models.CharField(max_length=250)  # the event that took place in the mobile application
    timestamp = models.DateTimeField(default=timezone.now, blank=True)  # the timestamp at which the even was logged

    class Meta:
        verbose_name_plural = 'analytics'

    def __str__(self):
        return self.event + ' recorded for ' + str(self.participant)
