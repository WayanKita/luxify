from django.urls import path, re_path
from . import views
from rest_framework_swagger.views import get_swagger_view

app_name = "floorPlan"


schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    re_path(r'^room/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='room-detail'),
    re_path(r'^room/(?P<pk>[0-9]+)/delete/$', views.RoomDelete.as_view(), name='room-delete'),
    re_path(r'^$', views.sandbox, name='sandbox'),
    re_path(r'^add_user/$', views.UserFormView.as_view(), name='person-add'),
    re_path(r'^android_add_user/$', views.UserAPI.as_view(), name='android-add'),
    re_path(r'^add_room/$', views.RoomCreate.as_view(), name='room-add'),
    re_path(r'^add_table/$', views.TableCreate.as_view(), name='table-add'),
    re_path(r'^add_chair/$', views.ChairCreate.as_view(), name='chair-add'),
    re_path(r'^add_window/$', views.WindowCreate.as_view(), name='window-add'),
    re_path(r'^api_tester$', schema_view)
]



