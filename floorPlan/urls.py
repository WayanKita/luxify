from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = "floorPlan"

# all URL patterns on the website
urlpatterns = [
    # root URL
    re_path(r'^$', views.index, name='index'),

    # API URLs
    re_path(r'^android_add_user/$', views.RegisterAPI.as_view(), name='android-add'),
    # re_path(r'^android_alertness_questionnaire/$', views.AlertnessQuestionnaireAPI.as_view(), name='android-alert'),
    # re_path(r'^android_demographic_questionnaire/$', views.DemographicQuestionnaireAPI.as_view(), name='android-alert'),
    re_path(r'^android_login/$', views.LoginAPI.as_view(), name='android-login'),
    re_path(r'^android_room/$', views.RoomAPI.as_view(), name='android-room'),
    re_path(r'^android_sensor/$', views.SensorAPI.as_view(), name='android-sensor'),
    re_path(r'^android_desk/$', views.TableAPI.as_view(), name='android-desk'),
    re_path(r'^add_user/$', views.ParticipantFormView.as_view(), name='person-add'),
    re_path(r'^android_window/$', views.WindowAPI.as_view(), name='android-window'),
    re_path(r'^android_room_generator/$', views.RoomGeneratorAPI.as_view(), name='android-window'),

    # Create URLs
    re_path(r'^add_chair/$', views.ChairCreate.as_view(), name='chair-add'),
    re_path(r'^add_room/$', views.RoomCreate.as_view(), name='room-add'),
    re_path(r'^add_sensor/$', views.SensorCreate.as_view(), name='sensor-add'),
    re_path(r'^add_desk/$', views.DeskCreate.as_view(), name='desk-add'),
    re_path(r'^add_window/$', views.WindowCreate.as_view(), name='window-add'),

    # Delete URLs
    re_path(r'^room/(?P<pk>[0-9]+)/delete/$', views.RoomDelete.as_view(), name='room-delete'),

    # Detail view URLs
    re_path(r'^room/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='room-detail'),

]