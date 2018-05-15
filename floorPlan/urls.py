from django.urls import path, re_path
from . import views

app_name = "floorPlan"

urlpatterns = [
    re_path(r'^room/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='room-detail'),
    re_path(r'^room/(?P<pk>[0-9]+)/delete/$', views.RoomDelete.as_view(), name='room-delete'),
    re_path(r'creator/$', 'views.sandbox', name='sandbox'),
dhdhdhy
    re_path(r'creator/add_user/$', views.UserFormView.as_view(), name='person-add'),
    re_path(r'creator/add_room/$', views.RoomCreate.as_view(), name='room-add'),
    re_path(r'creator/add_table/$', views.TableCreate.as_view(), name='table-add'),
    re_path(r'creator/add_chair/$', views.ChairCreate.as_view(), name='chair-add'),
    re_path(r'creator/add_window/$', views.WindowCreate.as_view(), name='window-add'),
]



