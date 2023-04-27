from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/sherlock/', views.sherlock_api, name='sherlock_api'),
]