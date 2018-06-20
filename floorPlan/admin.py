from django.contrib import admin
from django.http import HttpResponse
from .models import *
import csv

# TODO: remove edit rights to views in admin panel
# TODO: fix typo on inlines

def do_download(model, all_objects):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format('test')
    writer = csv.writer(response)

    fields = [field for field in model.get_fields() if not field.many_to_many and not field.one_to_many]
   
    writer.writerow([field.name for field in fields])
   
    for desk in all_objects:
        row = []
        for field in fields:
            field_value = getattr(desk, field.name)
            row.append(field_value)

        writer.writerow(row)
    return response


def download_alertness_questionnaire(modeladmin, request, queryset):
    return do_download(AlertnessQuestionnaire._meta, AlertnessQuestionnaire.objects.all())


def download_demographic_questionnaire(modeladmin, request, queryset):
    return do_download(DemographicQuestionnaire._meta, DemographicQuestionnaire.objects.all())


def download_sensor_history(modeladmin, request, queryset):
    return do_download(SensorHistory._meta, SensorHistory.objects.all())


def download_analytics(modeladmin, request, queryset):
    return do_download(Analytics._meta, Analytics.objects.all())


class WindowInline(admin.TabularInline):
    model = Window


class DoorInline(admin.TabularInline):
    model = Door


class DeskInline(admin.TabularInline):
    model = Desk


class RoomAdmin(admin.ModelAdmin):
    inlines = [
        WindowInline,
        DoorInline,
        DeskInline,
    ]


class SensorAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False


class SensorHistoryAdmin(admin.ModelAdmin):
    actions = [download_sensor_history]

    def has_add_permission(self, request):
        return False


class AlertnessQuestionnaireAdmin(admin.ModelAdmin):
    actions = [download_alertness_questionnaire]

    def has_add_permission(self, request):
        return False


class DemographicQuestionnaireAdmin(admin.ModelAdmin):
    actions = [download_demographic_questionnaire]

    def has_add_permission(self, request):
        return False

class AnalyticsAdmin(admin.ModelAdmin):
    actions = [download_analytics]

    def has_add_permission(self, request):
        return False


# Allows the admin to edit thee following tables on url [...]/admin
admin.site.register(Room, RoomAdmin)
admin.site.register(Participant)
admin.site.register(Sensor, SensorAdmin)  # sensors are automatically created
admin.site.register(SensorHistory, SensorHistoryAdmin)
admin.site.register(AlertnessQuestionnaire, AlertnessQuestionnaireAdmin)
admin.site.register(DemographicQuestionnaire, DemographicQuestionnaireAdmin)
admin.site.register(ParticipantProfiles)
admin.site.register(Analytics, AnalyticsAdmin)
admin.site.register(UserCategory)
admin.site.register(Layout)
admin.site.register(AlertnessTime)
admin.site.register(Recommendation)
