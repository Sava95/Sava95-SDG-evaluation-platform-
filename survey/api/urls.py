from django.conf.urls import url
from django.urls import path, include
from .views import (
    SdgScoreApiView,
)

urlpatterns = [
    path('', SdgScoreApiView.as_view()),
]