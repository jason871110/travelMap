
# Create your models here.
from __future__ import unicode_literals
from django.db import models


# Create your models here.

class Schedule(models.Model):
    id_num = models.IntegerField(blank=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100,blank=True)
    content = models.CharField(max_length=1000,blank=True)
    style = models.CharField(max_length=100,blank=True)
    days = models.IntegerField(blank=True)
    image = models.CharField(max_length=100,blank=True)

    #created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TotalCourse(models.Model):
    day = models.IntegerField(blank=True)
    course = models.ForeignKey(Schedule,    on_delete=models.CASCADE)

    def __str__(self):
        if (self.day!=0):
            return 'Day'+str(self.day)
        else:
            return '我的最愛'

class TouristSite(models.Model):
    route_order = models.IntegerField()
    site_name = models.CharField(max_length=100)
    site_id = models.IntegerField(blank=True)
    time =  models.TextField(blank=True)
    image = models.CharField(max_length=100,blank=True)
    line = models.ForeignKey(TotalCourse,    on_delete=models.CASCADE)
    location = models.CharField(max_length=100,blank=True)
    site_content = models.TextField(blank=True)

    class Meta:
         ordering = ['route_order']
    def __str__(self):
        return self.site_name

class IMG(models.Model):
    img = models.ImageField(upload_to='upload')
