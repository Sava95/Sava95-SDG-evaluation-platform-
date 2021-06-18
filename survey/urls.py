from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('survey/', views.survey, name='survey'),
    path('sectors/', views.sectors, name='sectors'),
    path('comparison/', views.comparison, name='comparison'),
    path('comments/', views.comments, name='comments'),
    path('instructions/', views.instructions, name='instructions'),
    path('charts/', views.comment_data, name='charts'),
    path('scores/', views.scores, name='scores'),
    path('relevance_result/', views.relevance_result, name='relevance_result'),
    path('api/', include('survey.api.urls')),
    path('get_sof/', views.get_sof, name='get_sof')
]

