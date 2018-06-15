from django.contrib import admin
from .models import *

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

# Allows the admin to edit thee following tables on url [...]/admin
admin.site.register(Room, RoomAdmin)
admin.site.register(Participant)
admin.site.register(Sensor, SensorAdmin) # sensors are automatically created
admin.site.register(Sensor_History)
admin.site.register(AlertnessQuestionnaire)
admin.site.register(DemographicQuestionnaire)
admin.site.register(ParticipantProfiles)
admin.site.register(Analytics)
admin.site.register(UserCategory)
admin.site.register(Layout)
