
# Create your models here.
from __future__ import unicode_literals
from django.db import models


# Create your models here.
class Schedule(models.Model):
    id_num = models.IntegerField(blank=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100,blank=True)
    days = models.IntegerField(blank=True)
    style = models.CharField(max_length=100)
    image = models.ImageField(upload_to='upload',blank=True)
    content = models.CharField(max_length=200,blank=True)
    #created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TotalCourse(models.Model):
    day = models.IntegerField(blank=True)
    course = models.ForeignKey(Schedule,    on_delete=models.CASCADE)

    def __str__(self):
        return 'Day'+str(self.day)

class TouristSite(models.Model):
    route_order = models.IntegerField()
    site_name = models.CharField(max_length=100)
    time =  models.TextField(blank=True)
    image = models.ImageField(upload_to='upload',blank=True)
    line = models.ForeignKey(TotalCourse,    on_delete=models.CASCADE)
    location = models.CharField(max_length=100,blank=True)
    site_content = models.TextField(blank=True)

    class Meta:
         ordering = ['route_order']
    def __str__(self):
        return self.site_name

class IMG(models.Model):
    img = models.ImageField(upload_to='upload')

class MapSite(models.Model):
    name = models.CharField(max_length=100)
    site_type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    stay = models.IntegerField(blank=True,default=30)
    image = models.ImageField(upload_to='upload',blank=True)

    def __str__(self):
        return self.name