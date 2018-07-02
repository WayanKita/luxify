from django.urls import path, re_path
from . import views

app_name = 'app'

urlpatterns = [
    path('room/', views.RoomListView.as_view()),
    path('room/<pk>/', views.RoomDetailView.as_view()),
    path('desk/<pk>/', views.DeskView.as_view()),
    path('demographic_questionnaire/', views.QuestionnaireView.as_view()),
    path('analytics/', views.AnalyticsView.as_view()),
    path('alertness_interval/', views.AlertnessIntervalView.as_view()),
    path('alertness_questionnaire/', views.AlertnessQuestionnaireAnswerView.as_view()),
    path('demographic_questionnaire_answer/', views.QuestionnaireAnswerView.as_view()),
    path('register/', views.CreateParticipantView.as_view()),
    re_path(
        r'^participant/(?P<username>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$',
        views.ParticipantView.as_view()),
    re_path(
        r'^recommendation/(?P<username>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$',
        views.RecommendationView.as_view()),
    re_path(
        r'^category/(?P<username>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$',
        views.CategoryView.as_view()),
]
