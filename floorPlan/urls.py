from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from . import views

app_name = "floorPlan"

# all URL patterns on the website
urlpatterns = [
    # root URL
    re_path(r'^$', login_required(views.home), name='home'),

    # API URLs
    re_path(r'^API/register/$', views.RegisterUserAPI.as_view(), name='android-add'),
    re_path(r'^API/alertness_questionnaire/$', views.AlertnessQuestionnaireAPI.as_view(), name='android-alert'),
    re_path(r'^API/analytic/$', views.AnalyticsAPI.as_view(), name='android-analytic'),
    re_path(r'^API/demographic_questionnaire/$', views.DemographicQuestionnaireAPI.as_view(), name='android-alert'),
    re_path(r'^API/questionnaire_check/(?P<key>[0-9]+)/$', views.QuestionnaireCheckAPI.as_view(), name='android-check'),
    re_path(r'^API/room/(?P<pk>[0-9]+)/$', views.RoomAPI.as_view(), name='room-detail'),
    #re_path(r'^API/chair/(?P<pk>[0-9]+)/$', views.ChairAPI.as_view(), name='room-detail'),
    re_path(r'^API/sensor_table/(?P<pk>[0-9]+)/$', views.SensorTableAPI.as_view(), name='android-sensor'),
    re_path(r'^API/sensor_user/(?P<pk>[0-9]+)/$', views.SensorUserAPI.as_view(), name='android-sensor'),
    re_path(r'^API/desk/(?P<pk>[0-9]+)/$', views.DeskAPI.as_view(), name='android-desk'),
    re_path(r'^API/window/(?P<pk>[0-9]+)/$', views.WindowAPI.as_view(), name='android-window'),
    re_path(r'^API/user/(?P<user>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.UserAPI.as_view(), name='user'),
    re_path(r'^API/workspace/$', views.WorkspaceAPI.as_view(), name='android-workspace'),
    re_path(r'^API/room_generator/(?P<pk>[0-9]+)/$', views.RoomGeneratorAPI.as_view(), name='android-window'),
    re_path(r'^API/recommend_desk/(?P<user>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.RecommendDeskAPI.as_view(), name='android-window'),
    re_path(r'^API/set_occupancy/$', views.SetOccupancyAPI.as_view(), name='android-window'),
    re_path(r'^API/user_category/(?P<user>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.UserCategoryAPI.as_view(), name='android-window'),

    # Create URLs
    re_path(r'^room_plan/$', login_required(views.room_plan), name='room-plan'),
    re_path(r'^room_plan/add_chair/$', login_required(views.ChairCreate.as_view()), name='chair-add'),
    re_path(r'^room_plan/add_room/$', login_required(views.RoomCreate.as_view()), name='room-add'),
    re_path(r'^room_plan/add_sensor/$', login_required(views.SensorCreate.as_view()), name='sensor-add'),
    re_path(r'^room_plan/add_desk/$', login_required(views.DeskCreate.as_view()), name='desk-add'),
    re_path(r'^room_plan/add_user/$', login_required(views.ParticipantFormView.as_view()), name='person-add'),
    re_path(r'^room_plan/add_window/$', login_required(views.WindowCreate.as_view()), name='window-add'),

    # Delete URLs
    re_path(r'^room_plan/room_(?P<pk>[0-9]+)/delete/$', views.RoomDelete.as_view(), name='room-delete'),

    # Detail view URLs
    re_path(r'^room/(?P<pk>[0-9]+)/$', login_required(views.DetailView.as_view()), name='room-detail'),
    re_path(r'^data/alertness_questionnaire/$', login_required(views.alertness_questionnaire), name='alertness-detail'),
    re_path(r'^data/demographic_questionnaire/$', login_required(views.demographic_questionnaire), name='demographic-detail'),
    re_path(r'^data/user/$', login_required(views.user), name='user-detail'),
    re_path(r'^data/analytics/$', login_required(views.analytics), name='analytics-detail'),
    re_path(r'^data/download/$', login_required(views.send_file), name='download'),

    # Login URL
    re_path(r'^login/$', auth_views.LoginView.as_view(
        template_name='floorPlan/login.html'), name='login'),
    re_path(r'^logout/$', auth_views.logout, name='logout'),

    # Download link
    # re_path(r'^static/example.txt', download_csv),

    # Settings URL
    re_path(r'^settings/user_category/$', login_required(views.user_category), name='user-cat-setting'),
    re_path(r'^settings/alertness/$', login_required(views.alertness), name='alertness-setting'),
    re_path(r'^settings/demographic/$', login_required(views.DemographicCreate.as_view()), name='demographic-setting'),

]