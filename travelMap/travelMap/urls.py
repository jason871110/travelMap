"""travelMap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.urls import path
# from django.contrib import admin
# from django.contrib.auth.views import LoginView
from django.conf.urls.static import static
from django.conf import settings
from travel.views import show
from travel.views import develop, search_dis, sch
from travel.views import login, logout, register, filter_, extract_article, show_result, display, profile

urlpatterns = [
    url(r'^develop', develop),
    url(r'^search', search_dis),
    path('sch/<int:id_num>', sch),
    path('show/<slug:slug>', show),
    url(r'^filter', filter_, name='filter'),
    url(r'^result', show_result),
    url(r'^display/(?P<input_day>[-\w]+)/$', display, name="display"),
    url(r'^display/', display),
    url(r'^article', extract_article),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),
    url(r'^accounts/register/$', register),
    url(r'^profile', profile),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL)
