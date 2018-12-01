from __future__ import unicode_literals
# Create your views here.

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import TouristSite,Schedule,TotalCourse,IMG
from django.template.context import RequestContext
from django.http import JsonResponse
import json
from jieba_space import jieba_test
import os

# Create your views here.

result = []
def uploadImg(request):
    if request.method == 'POST':
        new_img = IMG(image=request.FILES.get('img'))
        #後面的'img'對應到html的name='img'
        new_img.save()
        return redirect('showimg.html')#view or html is ok

    return render(request,'uploadimg.html')


def showImg(request):
    imgs = IMG.objects.all()
    content = {
        'imgs':imgs,
    }
    return render(request,'showimg.html', content)

def insertNewSchedule(request):
    content = {}
    if request.method == 'POST':
        content['title'] = request.POST['title']
        content['author'] = request.POST['author']
        content['days'] =  request.POST['days']
        content['location'] = request.POST['location']
        content['course_content'] = request.POST['course_content']
        print(content['title'])
        #newCourse =  addNewCourseToDatabase(content)
        #return JsonResponse({"key": "value"})
        #return render(request,'create_course.html', content)
        return JsonResponse(content, safe=False)

    return render(request,'create_course.html')
def editSchedule(request):
    content = {}
    if request.method == 'POST':
        content['title'] = request.POST['title']
        content['author'] = request.POST['author']
        content['days'] =  request.POST['days']
        content['location'] = request.POST['location']
        content['course_content'] = request.POST['course_content']
        #newCourse =  addNewCourseToDatabase(content)
        #return JsonResponse({"key": "value"})
        return render(request,'edit_schedule.html', content)

    return render(request,'edit_schedule.html')

def addCourseLines(request):
    content = {}
    
    if request.method == 'POST':
        if(request.POST['whichday']=='dayone'):
            content['day'] = 1
        elif(request.POST['whichday']=='daytwo'):
            content['day'] = 2
        elif(request.POST['whichday']=='daythree'):
            content['day'] = 3
        content['site_content'] = request.POST['site_content']

        #content['pk'] = request.POST['pk']#need to be added by html or javascript
        #newLine = addNewLineToDatabase(content)
        sites = []
        i=0
        
        for loc in range(0,7):
            i = loc+1
            string = 'small_location{0}'.format(i)
            if(request.POST[string]):
                sites.append(request.POST[string])

        #print(sites)
    content['pk']= 6
    return render(request,'add_lines.html',content)

def show_result(request):
    results = result
    render(request,'result.html',locals())

def extract_article(request):
    if request.method == 'POST':
        sentence = request.POST['article']
        result = jieba_test.find_sites(sentence)
        print(result)
        return render(request,'result.html',locals())
    return render(request,'extract.html')

def addNewScheduleToDatabase(content):
    obj = Schedule.objects.create(title=content['title'],author=content['author'],days=content['days'],
                location=content['location'],course_content=content['course_content'])
    return obj

def addNewLineToDatabase(content):
    obj = TotalCourse.objects.create(title=content['day'],site_content=content['site_content'],Course=content['pk'])
    
    return obj

