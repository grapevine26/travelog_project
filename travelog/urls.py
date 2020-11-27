"""travelog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('join', Join.as_view(), name='join'),
    path('login', Login.as_view(), name='login'),
    path('who_are_we', WhoAreWe.as_view(), name='who_are_we'),
    path('memories', Memories.as_view(), name='memories'),
    path('memories_detail', MemoriesDetail.as_view(), name='memories_detail'),
    path('memories_write', MemoriesWrite.as_view(), name='memories_write'),
    path('footprints', FootPrints.as_view(), name='footprints'),
    path('tips', Tips.as_view(), name='tips'),
    path('contact', Contact.as_view(), name='contact'),
]
