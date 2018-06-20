from django.contrib import admin
from .models import *
from django.http import HttpResponse
import csv

def download_survey(modeladmin, request, queryset):
    return do_download(Survey._meta, Survey.objects.all())


def download_question(modeladmin, request, queryset):
    return do_download(Question._meta, Question.objects.all())


class SurveyAdmin(admin.ModelAdmin):
    actions = [download_survey]


class QuestionAdmin(admin.ModelAdmin):
    actions = [download_question]


# Allows the admin to edit thee following tables on url [...]/admin
#admin.site.register(Category)
admin.site.register(Question, QuestionAdmin)
#admin.site.register(Answer)
#admin.site.register(Response)
admin.site.register(Survey, SurveyAdmin)
