from __future__ import unicode_literals
from django.db import models


# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100,blank=True)
    content = models.TextField(blank=True)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TouristSite(models.Model):
    site_name = models.CharField(max_length=100)
    route_order = models.IntegerField()
    image = models.ImageField(upload_to='upload',blank=True)
    course = models.ForeignKey(Course)

    def __str__(self):
        return self.site_name



