from email.mime import base
from posixpath import basename
from django.contrib import admin
from django.urls import path, include
from usermodule.views import UserViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]