from django.contrib import admin

# Register your models here.
from .models import Schedule,TotalCourse,TouristSite,MapSite
admin.site.register(Schedule)
admin.site.register(TotalCourse)
admin.site.register(TouristSite)
admin.site.register(MapSite)