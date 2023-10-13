from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import *

urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view()),
    path('auth/register/', RegisterView.as_view()),
    path('services/', Service.as_view()),
    path('services/<str:status>', ServicesStatus.as_view()),
]