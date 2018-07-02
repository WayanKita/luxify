from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from app.models.room import Desk, Door, Window, Room, Sensor, SensorLog
from app.models.questionnaire import Questionnaire, Question, Choice
from app.models.preference import AlertnessInterval
from app.models.participant import \
    Participant, Category, Profile, QuestionnaireAnswer, \
    AlertnessQuestionnaireAnswer, Analytics
import csv


"""
This file defines the editors viewable in the admin panel
"""


def do_download(model, all_objects):

    """
    Exports data to CSV files
    """

    response = HttpResponse(content_type='text/csv')  # the response time
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format('test')  
    writer = csv.writer(response) 

    fields = [
        field for field in model.get_fields() 
        if not field.many_to_many and not field.one_to_many
    ]
   
    writer.writerow([field.name for field in fields])
   
    for item in all_objects:
        row = []
        for field in fields:
            field_value = getattr(item, field.name)
            row.append(field_value)

        writer.writerow(row)
    return response


def download_alertness_questionnaire_answers(modeladmin, request, queryset):
    """ 
    Exports alertness questionnaire data 
    """
    return do_download(AlertnessQuestionnaireAnswer._meta, AlertnessQuestionnaireAnswer.objects.all())


def download_questionnaire_answers(modeladmin, request, queryset):
    """ 
    Exports demographic questionnaire data 
    """
    return do_download(QuestionnaireAnswer._meta, QuestionnaireAnswer.objects.all())


def download_sensor_log(modeladmin, request, queryset):
    """ 
    Exports sensor log data 
    """
    return do_download(SensorLog._meta, SensorLog.objects.all())


def download_analytics(modeladmin, request, queryset):
    """ 
    Exports analytics data 
    """
    return do_download(Analytics._meta, Analytics.objects.all())


def download_participant(modeladmin, request, queryset):
    """ 
    Exports participant data 
    """
    return do_download(Participant._meta, Participant.objects.all())


class DeskInline(admin.TabularInline):
    """
    Enables the inline view of desks in the room editor
    """
    model = Desk  # the model to show an inline view of


class DoorInline(admin.TabularInline):

    """
    Enables the inline view of doors in the room editor
    """

    model = Door  # the model to show an inline view of
    extra = 1  # the default number of fields to show on creation


class WindowInline(admin.TabularInline):

    """
    Enables the inline view of windows in the room editor
    """

    model = Window  # the model to show an inline view of
    extra = 1  # the default number of fields to show on creation


class RoomAdmin(admin.ModelAdmin):

    """
    Adds the inline views of desks, doors, and windows to the room editor
    """

    inlines = [
        DeskInline,
        DoorInline,
        WindowInline,
    ]


class AlertnessQuestionnaireAnswerAdmin(admin.ModelAdmin):
    actions = [download_alertness_questionnaire_answers]

    def has_add_permission(self, request):
        return False


class QuestionnaireAnswerAdmin(admin.ModelAdmin):
    actions = [download_questionnaire_answers]

    def has_add_permission(self, request):
        return False


class AnalyticsAdmin(admin.ModelAdmin):
    actions = [download_analytics]

    def has_add_permission(self, request):
        return False


class ParticipantAdmin(admin.ModelAdmin):
    actions = [download_participant]

    def has_add_permission(self, request):
        return False


class ChoiceInline(admin.TabularInline):

    """
    Enables the inline view of answer choices in the question editor
    """

    model = Choice


class QuestionAdmin(admin.ModelAdmin):

    """
    Adds the inline views of answer choices to the question editor 
    """

    inlines = [
        ChoiceInline,
    ]


class SensorAdmin(admin.ModelAdmin):

    """
    Prevents the editing of sensors (these are imported automatically)
    """

    def has_add_permission(self, request):
        return False


class SensorLogAdmin(admin.ModelAdmin):
    actions = [download_sensor_log]

    def has_add_permission(self, request):
        return False


class UserProfileAdmin(UserAdmin): 
    exclude = ('first_name', 'last_name', 'email', 'is_superuser', 'user_permissions')
    fieldsets = (
        ('Information', {'fields': ('username', 'password')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups',)}),
    )


admin.site.site_header = 'Luxify Admin'  # change the header title in the admin panel
admin.site.register(Room, RoomAdmin)  # add a room editor to the admin panel
admin.site.register(Sensor, SensorAdmin)  # add a sensor editor to the admin panel
admin.site.register(SensorLog, SensorLogAdmin)  # add a sensor log editor to the admin panel
admin.site.register(Participant, ParticipantAdmin)  # add a participant editor to the admin panel
admin.site.register(Category)  # add a user cateogry editor to the admin panel
admin.site.register(Questionnaire)  # add a questionnaire editor to the admin panel
admin.site.register(Question, QuestionAdmin)  # add a question editor to the admin panel
admin.site.register(Profile)  # add a profile editor to the admin panel
admin.site.register(QuestionnaireAnswer, QuestionnaireAnswerAdmin)  # add questionnaire answers to the admin panel
admin.site.register(AlertnessQuestionnaireAnswer, AlertnessQuestionnaireAnswerAdmin)  # add an alertness questionnaire answers to the admin panel
admin.site.register(AlertnessInterval)  # add an alertness questionnaire editor to the admin panel
admin.site.register(Analytics, AnalyticsAdmin)  # add analytics to the admin panel
