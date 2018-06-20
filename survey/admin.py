from django.contrib import admin
from .models import *

# Allows the admin to edit thee following tables on url [...]/admin
#admin.site.register(Category)
admin.site.register(Question)
#admin.site.register(Answer)
#admin.site.register(Response)
admin.site.register(Survey)
