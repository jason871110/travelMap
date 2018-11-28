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
from travel.views import uploadImg,showImg,insertNewSchedule,addCourseLines,addNewScheduleToDatabase,ind,schedule
from travel.views import login, logout, register, drag, query,form
from django.views.generic import TemplateView
from travel.views import sch
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', uploadImg),
    url(r'^upload', uploadImg),
    url(r'^show', showImg),
    url(r'^insert', insertNewSchedule),
    url(r'^addline', addCourseLines),
    path('index',ind),
    path('schedule',schedule),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),
    url(r'^accounts/register/$', register),
    url(r'drag',drag),
    url(r'query/$',query),
    url(r'form',form),
    url(r'ns',sch),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
