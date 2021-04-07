"""Theta URL Configuration

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
from django.urls import path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path('', views.HomeView.as_view()),
    path('admin/', admin.site.urls),
    url(r'^api/profile/', views.ProfileEndpoint.as_view()),
    url(r'^api/chat/', views.ChatEndpoint.as_view()),
    url(r'^api/config/', views.ConfigEndpoint.as_view()),
    url(r'^api/timer/', views.TimerEndpoint.as_view()),
    url(r'^api/auth/', views.AuthEndpoint.as_view()),
    url(r'^api/auth/refresh/', views.RefreshEndpoint.as_view()),
    url(r'^api/giftable/get/', views.GetGiftableEndpoint.as_view()),
    url(r'^api/giftable/gift/', views.GiftGiftableEndpoint.as_view()),
    url(r'^api/send/chat/', views.SendChatEndpoint.as_view()),
    url(r'^api/user/', views.GetUserEndpoint.as_view()),
    url(r'^api/user/chat/', views.UserChatEndpoint.as_view()),
    url(r'^api/channel/follow/', views.FollowChannelEndpoint.as_view()),
    url(r'^api/xp/', views.UserXPEndpoint.as_view()),
    url(r'^api/reward/new/', views.NewRewardEndpoint.as_view()),
    url(r'^api/reward/edit/', views.EditRewardEndpoint.as_view()),
    url(r'^api/reward/delete/', views.DeleteRewardEndpoint.as_view()),
    url(r'^api/show/reward/', views.ShowRewardEndpoint.as_view()),
    url(r'^api/rewards/', views.MyRewardsEndpoint.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
