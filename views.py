from __future__ import unicode_literals
# Create your views here.
import json
# import requests
import re
from django.shortcuts import render, redirect, render_to_response
# from django.urls import reverse
# from django.template import RequestContext
from .models import TouristSite, IMG, Schedule, TotalCourse
from django.db.models import Max
from django.http import JsonResponse, HttpResponse
# from django.db.models import Count
from jieba_space import jieba_test
# import static
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django import forms
import random
import requests
from PIL import Image
from io import BytesIO




def develop(request):

    schedule_idset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    random.shuffle(schedule_idset)
    schedule_item = list()
    for i in range(0, len(schedule_idset)):
        schedule_item.append(Schedule())
        schedule_item[i] = Schedule.objects.get(id_num=schedule_idset[i])

    return render_to_response('develop.html', {'schedule_item': schedule_item})


def search_dis(request):
    return render_to_response('display.html')


def sch(request,id_num):
    schedule_now = Schedule.objects.get(id=id_num)
    print(schedule_now.title)
    schedule_all_course= schedule_now.totalcourse_set.all()
    print(schedule_all_course)
    max_day = schedule_all_course.aggregate(Max('day'))['day__max']
    print(max_day)


    content={}
    if request.method == 'GET':
        content['max_day'] = max_day
        schedule_all_course_by_day = []
        course_tem=[]
        for i in range(max_day):
            course_tem=schedule_all_course.get(day=i + 1).touristsite_set.all()
            schedule_all_course_by_day.append(course_tem)
        content['site_information'] = schedule_all_course_by_day
        print(content['site_information'])

    if request.method == 'POST':
        if request.POST.get('type','') == 'change_day':
            order = request.POST.get('sorted_order', '')
            day_cur = request.POST.get('day_cur', '')
            order=re.findall(r'[0-9]+', order)
            order=order[:-1]
            print(len(order))
            i = 0
            while ( i < len(order) ):
                try:
                    temp = TouristSite.objects.get(site_id=order[i])
                    # if (int(temp.line) != line_id):
                    #    temp.line =  str(line_id)
                    temp.route_order = i
                    temp.save()
                    i += 1
                except:
                    i = len(order) + 1
            content['origin'] = {'placeId': TouristSite.objects.get(site_id=order[0]).location}
            content['destination'] = {'placeId': TouristSite.objects.get(site_id=order[len(order) - 1]).location}
            content['waypoints'] = []
            for i in range(1, len(order) - 1):
                print(i)
                content['waypoints'].append({'stopover': True, 'location': {'placeId':TouristSite.objects.get(site_id=order[i]).location}})
            return JsonResponse(content)
        elif request.POST.get('type','') == 'add_site':
            print(request.POST.get('site_name',''))
            place_id = search(request.POST.get('site_name',''))
            place_phone = detail(place_id)['phone_number']
            place_address = detail(place_id)['address']
            print(place_id)
            print(place_address)
            print(place_phone)
            schedule_all_course = schedule_now.totalcourse_set.all().get(day=request.POST.get('day_cur',''))
            return render_to_response('sch.html')
    return render_to_response('sch.html',content)

def search(name):

    url_temp = ("https://maps.googleapis.com/maps/api/place/findplacefromtext/json?" +
                "input=" + name +
                "&key=" + "AIzaSyB2pGT9ePkt26BbSk1tvcPWXg1_8ZZ8lM8" +
                "&inputtype=" + "textquery" +
                "&locationbias=" + "ipbias")
    res = requests.get(url_temp)
    # print(res)
    # print(type(res.content))
    # print(str(res.content))

    result = res.content.decode("utf-8")
    result = json.loads(result)
    # print(list(result))
    if (len(result["candidates"]) == 0):
        return None
    result_id = result['candidates'][0]["place_id"]

    return result_id
    # return None

def detail(place_id):
    url_temp = ('https://maps.googleapis.com/maps/api/place/details/json?'+
                'key=' + "AIzaSyB2pGT9ePkt26BbSk1tvcPWXg1_8ZZ8lM8" +
                '&placeid=' + place_id +
                '&language=zh-TW'+
                '')
    # print(url_temp)
    res = requests.get(url_temp)
    # print(res)
    result_json = json.loads(res.content.decode('utf-8'))
    if result_json['status'] != 'OK':
        return None
    # print(result_json)
    result = {}
    try:
        result['phone_number'] = result_json['result']['formatted_phone_number']
    except:
        result['phone_number'] = None
    try:
        result['address'] = result_json['result']['formatted_address']
    except:
        result['address'] = None

    return result

def camera(place_id):
    url_temp = ("https://maps.googleapis.com/maps/api/place/details/json?" +
                "placeid=" + place_id +
                "&key=" + "AIzaSyB2pGT9ePkt26BbSk1tvcPWXg1_8ZZ8lM8" +
                '')
    res = requests.get(url_temp)
    result = json.loads(res.content.decode('utf-8'))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    fo = open('detail.json', 'w')
    fo.write(json.dumps(result, ensure_ascii=False, indent=2))
    photo_reference = result['result']['photos'][0]['photo_reference']

    url_temp = ('https://maps.googleapis.com/maps/api/place/photo?' +
                'key=' + 'AIzaSyCS54PJ0zmirq0QNN29mKfPaJVE0KDCiTc' +
                '&photoreference=' + photo_reference +
                '&maxwidth=' + '600')

    res = requests.get(url_temp)
    content = BytesIO(res.content)

    print(content)
    print(type(content))
    picture = Image.open(content)
    picture.show()

