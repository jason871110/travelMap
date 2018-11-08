# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from .models import Course, TouristSite

# Create your views here.


def home(request):
    course_list = Course.objects.all()
    site_list = course_list[0].touristsite_set.all()
    img = site_list[0].image

    return render(request, 'home.html', {
    'course_list': course_list,
    'img':img,
            })

'''def uploadImg(request):
    if request.method == 'POST':
        new_img = IMG(
            img=request.FILES.get('img')
        )
        new_img.save()
        return redirect('uploadimg.html')#加redirect以防重新提交表單
    return render(request, 'uploadimg.html')

def showImg(request):
    imgs = IMG.objects.all()
    content = {
        'imgs':imgs,
    }
    return render(request, 'showimg.html', content)
'''