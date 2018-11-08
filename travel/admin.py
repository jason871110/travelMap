from __future__ import unicode_literals
from django.contrib import admin

# Register your models here.
from .models import Course, TouristSite

class CourseAdmin(admin.ModelAdmin):
    list_display = ('pk','title','author','location','created_at')

class TouristSiteAdmin(admin.ModelAdmin):
    list_display = ('course','site_name','image','route_order')

admin.site.register(Course,CourseAdmin)
admin.site.register(TouristSite,TouristSiteAdmin)