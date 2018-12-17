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
from travel.views import form, home, create_form, develop
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', uploadImg),
    url(r'^upload', uploadImg),
    url(r'^show', showImg),
    url(r'^insert', insertNewSchedule),
    url(r'^addline', addCourseLines),
    # url(r'^index.(?P<file_type>\w+)/$', ind),
    path('index', ind, name='index'),
    url(r'ns',sch),
    url(r'^article', extract_article),
    url(r'^form',form),
    url(r'^accounts/login/',LoginView.as_view(template_name='login.html'),name="login"),
    url(r'^accounts/logout/',logout),
    url(r'^accounts/register/$', register),
    url(r'^profiles/home', form),
    url(r'^compre_form', create_form),
    url(r'^develop', develop),
    #path('schedule/<int:id_num>', schedule, name='schedule'),
    path('main/<int:id_num>', main, name='main'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL)

