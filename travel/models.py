
# Create your models here.
from __future__ import unicode_literals
from django.db import models


# Create your models here.

class Schedule_content(models.Model):
    image = models.ImageField(blank=True)
    intro = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    seq = models.IntegerField(blank=True)
    day = models.IntegerField(blank=True)


class Schedule(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100,blank=True)
    days = models.IntegerField(blank=True)
    schedule_content = models.ForeignKey(Schedule_content,on_delete=models.CASCADE)
    #location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TotalCourse(models.Model):
    day = models.IntegerField(blank=True)
    site_content = models.TextField(blank=True)
    course = models.ForeignKey(Schedule,    on_delete=models.CASCADE)

    def __str__(self):
        return self.day

class TouristSite(models.Model):
    route_order = models.IntegerField()
    site_name = models.CharField(max_length=100)
    time =  models.TextField(blank=True)
    image = models.ImageField(upload_to='upload',blank=True)
    line = models.ForeignKey(TotalCourse,    on_delete=models.CASCADE)

    def __str__(self):
        return self.site_name

class IMG(models.Model):
    img = models.ImageField(upload_to='upload')