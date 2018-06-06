from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = "floorPlan"

# all URL patterns on the website
urlpatterns = [
    # root URL
    re_path(r'^$', views.home, name='home'),

    # API URLs
    re_path(r'^API/register/$', views.RegisterUserAPI.as_view(), name='android-add'),
    re_path(r'^API/alertness_questionnaire/$', views.AlertnessQuestionnaireAPI.as_view(), name='android-alert'),
    re_path(r'^API/analytic/$', views.AnalyticsAPI.as_view(), name='android-analytic'),
    re_path(r'^API/demographic_questionnaire/$', views.DemographicQuestionnaireAPI.as_view(), name='android-alert'),
    re_path(r'^API/questionnaire_check/(?P<pk>[0-9]+)/$', views.QuestionnaireCheckAPI.as_view(), name='android-check'),
    re_path(r'^API/room/(?P<pk>[0-9]+)/$', views.RoomAPI.as_view(), name='room-detail'),
    re_path(r'^API/sensor_table/(?P<pk>[0-9]+)/$', views.SensorTableAPI.as_view(), name='android-sensor'),
    re_path(r'^API/sensor_user/(?P<pk>[0-9]+)/$', views.SensorUserAPI.as_view(), name='android-sensor'),
    re_path(r'^API/desk/(?P<pk>[0-9]+)/$', views.DeskAPI.as_view(), name='android-desk'),
    re_path(r'^API/window/(?P<pk>[0-9]+)/$', views.WindowAPI.as_view(), name='android-window'),
    re_path(r'^API/workspace/$', views.WorkspaceAPI.as_view(), name='android-workspace'),
    re_path(r'^API/room_generator/(?P<pk>[0-9]+)/$', views.RoomGeneratorAPI.as_view(), name='android-window'),

    # Create URLs
    re_path(r'^room_plan/$', views.room_plan, name='room-plan'),
    re_path(r'^room_plan/add_chair/$', views.ChairCreate.as_view(), name='chair-add'),
    re_path(r'^room_plan/add_room/$', views.RoomCreate.as_view(), name='room-add'),
    re_path(r'^room_plan/add_sensor/$', views.SensorCreate.as_view(), name='sensor-add'),
    re_path(r'^room_plan/add_desk/$', views.DeskCreate.as_view(), name='desk-add'),
    re_path(r'^room_plan/add_user/$', views.ParticipantFormView.as_view(), name='person-add'),
    re_path(r'^room_plan/add_window/$', views.WindowCreate.as_view(), name='window-add'),

    # Delete URLs
    re_path(r'^room_plan/room_(?P<pk>[0-9]+)/delete/$', views.RoomDelete.as_view(), name='room-delete'),

    # Detail view URLs
    re_path(r'^room/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='room-detail'),
    re_path(r'^data/alertness_questionnaire/$', views.alertness_questionnaire, name='alertness-detail'),
    re_path(r'^data/demographic_questionnaire/$', views.demographic_questionnaire, name='demographic-detail'),
    re_path(r'^data/user/$', views.user, name='user-detail'),

]