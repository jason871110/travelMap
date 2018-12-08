from __future__ import unicode_literals
# Create your views here.

from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import TouristSite,Schedule,TotalCourse,IMG
from django.template.context import RequestContext
from django.http import JsonResponse
from django.urls import reverse
import json
from jieba_space import jieba_test
import os

# Create your views here.

result = []
site_result= {}
def ind(request):
    content={}
    if request.method == 'GET':
        
        #content['id_num']=Schedule_content.objects.all().aggregate(Max('id_num'))['id_num__max']+1
        return render(request, 'index.html',content)
    elif request.method == 'POST':
        if request.POST.get('keyword')!= None:
            content1 = []
            content2 = []
            content3 = []
            print(request.POST['keyword'])
            posts = TouristSite.objects.filter(site_name__contains=request.POST['keyword'])
            print(posts)
            if posts != None:
                for p in posts:
                    content1.append(p.line.course)#append schedules
                    print(p.line.course.id_num)
            print(content1)
            if content1 != None:
                for c in content1:
                    content2.append(c.totalcourse_set.all())#append days under this schedule
                for c in content2:
                    for cc in c:
                        print('content2:'+ str(cc))
                #print(content2[0][0])

                for c in content2:
                    for cc in c:
                        content3.append(cc.touristsite_set.all())
                print(content3)
                for c in content3:
                    print(c)
                    for cc in c:
                            print('content3:'+ str(cc)+ str(cc.line))

            return render(request,'search_result.html',{'result1':content1,'result2':content2,'result3':content3})
    return render(request, 'index.html')

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

def extract_article(request):#extract article to list tourist sites
    if request.method == 'POST':
        sentence = request.POST['article']
        #result = jieba_test.find_sites(sentence)
        result = ["知事官邸","赤崁樓","孔廟","台南觀候所","成功大學","六千牛肉湯","莉莉冰果室"]
        result = decide_course(result)
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

def main(request, id_num):
    content={}
    if request.method == 'GET':
        schedule_all = Schedule.objects.get(id_num=id_num)
        schedule_day_all = schedule_all.totalcourse_set.all()
        print(schedule_all.days)
        num_of_day = [0]*(schedule_all.days+1)

        for sche in schedule_day_all:
            for site in sche.touristsite_set.all():
                num_of_day[sche.day]+=1


        content['schedule_day_all']=schedule_day_all
        content['max_day']=schedule_all.days
        content['num_of_day']=num_of_day
        content['origin']=schedule_day_all.get(day=1).touristsite_set.all().get(route_order=1).location
        content['destination']=schedule_day_all.get(day=1).touristsite_set.all().get(route_order=num_of_day[1]).location
        content['waypoints']=[]
        for i in range(2,num_of_day[1]):
            content['waypoints'].append(schedule_day_all.get(day=1).touristsite_set.all().get(route_order=i).location)
        print(content['origin']+"%%%from get")
        return render(request, 'main.html', content)
    elif request.method == 'POST':
        if request.POST.get('keyword')!= None:
            content['site'] = request.POST['keyword']
            print('python:'+content['site'])
            return render(request,'search_result.html',locals())
        else:
            target_day = request.POST['day']
            schedule_all = Schedule.objects.get(id_num=id_num)
            schedule_day_all = schedule_all.totalcourse_set.all()
            print(schedule_all.days)
            num_of_day = [0] * (schedule_all.days + 1)

            for sche in schedule_day_all:
                for site in sche.touristsite_set.all():
                    num_of_day[sche.day] += 1

            content['schedule_day_all'] = schedule_day_all
            content['max_day'] = schedule_all.days
            content['num_of_day'] = num_of_day
            content['origin'] = schedule_day_all.get(day=target_day).touristsite_set.all().get(route_order=1).location
            content['destination'] = schedule_day_all.get(day=target_day).touristsite_set.all().get(
                route_order=num_of_day[int(target_day)]).location
            content['waypoints'] = []
            for i in range(2, num_of_day[int(target_day)]):
                content['waypoints'].append(schedule_day_all.get(day=target_day).touristsite_set.all().get(route_order=i).location)
            print(content['origin']+'%%%from post')
            return render(request,'main.html',content)
        #return render_to_response('main.html', content,context_instance = RequestContext(request))
        #return HttpResponseRedirect(reverse('main',kwargs={'id_num':0}))
    return render(request, 'main.html')


def decide_course(original_course):
    result = []
    site = []
    food = []
    with open('site_info.json', 'r', encoding='utf-8') as f:
        json_dict = json.loads(f.read(),encoding="utf-8")
        for dic in json_dict:
            if dic["sort"]=="site":
                site.append(dic["name"])
            elif dic["sort"]=="food":
                food.append(dic["name"])
        #print (site)

        number = 1
        
        for item in original_course:
            for sort in site:
                if item == sort:
                    result.append(item)
                    number = number + 1
            if number%5 == 0:
                break
        
        counter  = 2
        for item in original_course:
            for sort in food:
                if item == sort:
                    result.insert(counter, item)
                    counter = counter + 3
        print(result)       
    
    
    return result