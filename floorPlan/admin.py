from django.contrib import admin
from .models import *

class WindowInline(admin.TabularInline):
	model = Window

class DoorInline(admin.TabularInline):
	model = Door

class ChairInline(admin.TabularInline):
	model = Chair

class DeskInline(admin.TabularInline):
	model = Desk

class RoomAdmin(admin.ModelAdmin):
    inlines = [
	WindowInline,
	DoorInline,
	DeskInline,
    ]

# Allows the admin to edit thee following tables on url [...]/admin
admin.site.register(Room, RoomAdmin)
admin.site.register(Desk)
admin.site.register(Participant)
admin.site.register(Sensor_Table)
admin.site.register(Sensor_User)
admin.site.register(Window)
admin.site.register(Chair)
# admin.site.register(Door)
admin.site.register(AlertnessQuestionnaire)
admin.site.register(DemographicQuestionnaire)
admin.site.register(ParticipantProfiles)
admin.site.register(Analytics)
admin.site.register(UserCategory)
admin.site.register(Layout)
admin.site.register(Recommendation)
admin.site.register(AlertnessTime)

