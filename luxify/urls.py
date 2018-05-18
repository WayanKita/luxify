from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include
from floorPlan import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rooms/', views.RoomList.as_view()),
    path('floorPlan/', include('floorPlan.urls')),
    path(r'o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

]

urlpatterns = format_suffix_patterns(urlpatterns)