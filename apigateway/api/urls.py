from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view()),
    path('auth/register/', RegisterViewSet.as_view({'post': 'post'})),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path('auth/user/', UserInfo.as_view({'get': 'get'})),
    path('services/', Service.as_view({'get': 'get'})),
    path('services/<int:id>/process/', ServicesProcess.as_view({'post': 'post', 'get': 'get'})),
    path('docs/', get_swagger_view(title='iDoctor API'))
]