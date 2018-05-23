from django.contrib import admin
from .models import *

# Allows the admin to edit thee following tables on url [...]/admin
admin.site.register(Room)
admin.site.register(Table)
admin.site.register(Participant)
admin.site.register(Sensor)
