from django.contrib.auth.decorators import login_required
from django.urls import re_path
from django.contrib.auth import views as auth_views
from . import views


# TODO: write comments
# TODO: remove URLs linked to luxify website
# TODO: standardize APIs


app_name = "floorPlan"
urlpatterns = [

    re_path(r'^API/register/$', views.RegisterUserAPI.as_view(), name='android-add'),
    re_path(r'^API/alertness_questionnaire/$', views.AlertnessQuestionnaireAPI.as_view(), name='android-alert'),
    re_path(r'^API/analytic/$', views.AnalyticsAPI.as_view(), name='android-analytic'),
    re_path(r'^API/demographic_questionnaire/$', views.DemographicQuestionnaireAPI.as_view(), name='android-alert'),
    re_path(r'^API/questionnaire_check/(?P<key>[0-9]+)/$', views.QuestionnaireCheckAPI.as_view(), name='android-check'),
    # re_path(r'^API/sensor_table/(?P<pk>[0-9]+)/$', views.SensorTableAPI.as_view(), name='android-sensor'),
    re_path(r'^API/user/(?P<user>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.UserAPI.as_view(), name='user'),
    re_path(r'^API/user/(?P<user>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/name', views.UserNameAPI.as_view(), name='name'),
    re_path(r'^API/workspace/$', views.WorkspaceAPI.as_view(), name='android-workspace'),
    re_path(r'^API/room_generator/(?P<pk>[0-9]+)/$', views.RoomGeneratorAPI.as_view(), name='android-window'),
    re_path(r'^API/desk/(?P<pk>[0-9]+)/$', views.DeskAPI.as_view(), name='android-window'),
    re_path(r'^API/recommend_desk/(?P<user>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.RecommendDeskAPI.as_view(), name='android-window'),
    re_path(r'^API/set_occupancy/$', views.SetOccupancyAPI.as_view(), name='android-window'),
    re_path(r'^API/user_category/(?P<user>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.UserCategoryAPI.as_view(), name='android-window'),
    re_path(r'^API/alertness_interval/$', views.AlertnessIntervalAPI.as_view(), name='alertness-interval'),

]