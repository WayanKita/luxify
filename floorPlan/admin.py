from django.contrib import admin
from .models import *

# Allows the admin to edit thee following tables on url [...]/admin
admin.site.register(Room)
admin.site.register(Desk)
admin.site.register(Participant)
admin.site.register(Sensor_Table)
admin.site.register(Sensor_User)
admin.site.register(Window)
admin.site.register(Chair)
admin.site.register(Door)
admin.site.register(AlertnessQuestionnaire)
admin.site.register(DemographicQuestionnaire)
admin.site.register(ParticipantProfiles)
