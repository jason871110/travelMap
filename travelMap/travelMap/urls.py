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
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from travel.views import uploadImg, showImg, sch, main,insertNewSchedule, addCourseLines, addNewScheduleToDatabase, ind,extract_article
#from travel.views import form, login, logout
from django.contrib.auth.views import LoginView
from travel.views import logout, register
from travel.views import form, home, create_form, develop , display
urlpatterns = [
    url(r'^develop', develop),
    # url(r'^search', search_dis),
    url(r'^display/(?P<input_day>[-\w]+)/$', display, name="display")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL)

