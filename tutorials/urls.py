from django.contrib import admin
from django.urls import path, include

from tutorials import views

app_name = "tutorials"

urlpatterns = [
    path('', views.index, name="index"),
    path('topic/<int:pk>/', views.topic, name='topic_detail')
]