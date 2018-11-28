from __future__ import unicode_literals
# Create your views here.

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import TouristSite, IMG, Schedule, TotalCourse
from django.db.models import Max
from django.http import JsonResponse
from django.db.models import Count

import static
import json


def ind(request):
    if request.method == 'GET':
        content={}
        #content['id_num']=Schedule_content.objects.all().aggregate(Max('id_num'))['id_num__max']+1
        return render(request, 'index.html',content)


def uploadImg(request):
    if request.method == 'POST':
        new_img = IMG(img=request.FILES.get('img'))
        # 後面的'img'對應到html的name='img'
        new_img.save()
        return redirect('showimg.html')  # view or html is ok

    return render(request, 'uploadimg.html')


def showImg(request):
    imgs = IMG.objects.all()
    content = {
        'imgs': imgs,
    }
    return render(request, 'showimg.html', content)


def insertNewSchedule(request):
    content = {}
    if request.method == 'POST':
        content['title'] = request.POST['title']
        content['author'] = request.POST['author']
        content['days'] = request.POST['days']
        content['location'] = request.POST['location']
        content['course_content'] = request.POST['course_content']
        print(content['title'])
        # newCourse =  addNewCourseToDatabase(content)
        # return JsonResponse({"key": "value"})
        # return render(request,'create_course.html', content)
        return JsonResponse(content, safe=False)
    return render(request,'create_schedule.html')
    
def editSchedule(request):
    content = {}
    if request.method == 'POST':
        content['title'] = request.POST['title']
        content['author'] = request.POST['author']
        content['days'] = request.POST['days']
        content['location'] = request.POST['location']
        content['course_content'] = request.POST['course_content']
        # newCourse =  addNewCourseToDatabase(content)
        # return JsonResponse({"key": "value"})
        return render(request, 'edit_schedule.html', content)

    return render(request, 'edit_schedule.html')


def addCourseLines(request):
    content = {}

    if request.method == 'POST':
        if (request.POST['whichday'] == 'dayone'):
            content['day'] = 1
        elif (request.POST['whichday'] == 'daytwo'):
            content['day'] = 2
        elif (request.POST['whichday'] == 'daythree'):
            content['day'] = 3
        content['site_content'] = request.POST['site_content']

        # content['pk'] = request.POST['pk']#need to be added by html or javascript
        # newLine = addNewLineToDatabase(content)
        sites = []
        i = 0

        for loc in range(0, 7):
            i = loc + 1
            string = 'small_location{0}'.format(i)
            if (request.POST[string]):
                sites.append(request.POST[string])

        # print(sites)
    content['pk'] = 6
    return render(request, 'add_lines.html', content)


def addNewScheduleToDatabase(content):
    obj = Schedule.objects.create(title=content['title'], author=content['author'], days=content['days'],
                                  location=content['location'], course_content=content['course_content'])
    return obj


def addNewLineToDatabase(content):
    obj = TotalCourse.objects.create(title=content['day'],site_content=content['site_content'],Course=content['pk'])
    
    return obj


'''
def schedule(request,id_num):
    content = {}
    if request.method == 'GET':
        day_1_all = Schedule_content.objects.all().filter(id_num=id_num)
        content['day_1_all'] = day_1_all
        content['id_num']=id_num
        print(content['day_1_all'])
        print("adad")
        return render(request, 'schedule.html', content)

    if request.method == 'POST':
        if request.POST.get('rewrite') == '0':
            day_1_all = Schedule_content.objects.all().filter(id_num=id_num)
            content['day_1_all'] = day_1_all
            content['day'] = request.POST.get('whichday')
            content['seq'] = request.POST.get('seq')
            content['id_num']=id_num
            for sch in day_1_all:
                if sch.day == int(content['day']):
                    if sch.seq >= int(content['seq']):
                        upload_sch = Schedule_content.objects.get(day=sch.day, seq=sch.seq, title=sch.title,id_num=id_num)
                        upload_sch.seq += 1
                        upload_sch.save()

            content['title'] = request.POST['title']
            content['intro'] = request.POST['intro']
            # content['pk'] = request.POST['pk']#need to be added by html or javascript
            # newLine = addNewLineToDatabase(content)
            sites = []
            i = 0
            # print(sites)
            f = Schedule_content(day=content['day'], seq=content['seq'], title=content['title'], intro=content['intro'], id_num=id_num)
            f.save()
            # content['pk'] = 6
            day_1_all = Schedule_content.objects.all()
            content['day_1_all'] = day_1_all
            return HttpResponseRedirect(reverse('schedule',kwargs={'id_num':id_num}))
        elif request.POST.get('rewrite') == '1':
            day_1_all = Schedule_content.objects.all()
            for sch in day_1_all:
                if sch.day == int(content['day']):
                    if sch.seq == int(content['seq']):
                        upload_sch = Schedule_content.objects.get(day=sch.day, seq=sch.seq, title=sch.title, intro=sch.intro, id_num=id_num)
                        upload_sch.intro = request.POST.get('intro')
                        upload_sch.save()

            # content['pk'] = request.POST['pk']#need to be added by html or javascript
            # newLine = addNewLineToDatabase(content)
            sites = []
            i = 0
            # print(sites)
            # content['pk'] = 6
            return HttpResponseRedirect(reverse('schedule'))


        # return render(request, 'schedule.html', content)
'''
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
        return HttpResponseRedirect(reverse('main',kwargs={'id_num':0}))
    return render(request, 'main.html')
