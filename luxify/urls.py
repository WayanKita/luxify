from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include
from floorPlan import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # redirects floorPlan/* to the floorPlan app's urls.py file (floorPlan/urls.py)
    path('luxify/', include('floorPlan.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
