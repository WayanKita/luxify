from django.urls import path, re_path

from . import views

app_name = "floorPlan"

urlpatterns = [
    re_path(r'creator/$', views.sandbox, name='sandbox'),
    re_path(r'creator/add_room/$', views.RoomCreate.as_view(), name='room-add'),
    re_path(r'creator/add_table/$', views.TableCreate.as_view(), name='table-add'),
    re_path(r'creator/add_chair/$', views.ChairCreate.as_view(), name='chair-add'),
    re_path(r'creator/add_window/$', views.WindowCreate.as_view(), name='window-add'),
]