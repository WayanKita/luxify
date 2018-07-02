from django.db import models


"""
Questionnaire models
"""


class Questionnaire(models.Model):

    """
    Represents a questionnaire
    """

    name = models.CharField(max_length=250, unique=True)  # the name of the questionnaire

    def __str__(self):
        return self.name


class Question(models.Model):

    """
    Represents a question in a questionnaire
    """

    questionnaire = models.ForeignKey(
        Questionnaire,
        on_delete=models.CASCADE,
        related_name='questionnaire_question')  # the questionnaire the question belongs to
    question = models.CharField(max_length=250, unique=True)  # the question

    def __str__(self):
        return self.question


class Choice(models.Model):

    """
    Represents a question choice
    """

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='question_choice')  # the question this answer choice belongs to
    choice = models.CharField(max_length=250, unique=True)  # the answer choice

    def __str__(self):
        return self.choice
