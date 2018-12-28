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
    if request.method =='GET':
        return render_to_response('search.html')



def show(request,slug):
    print(slug)
    content={}
    if request.method == 'GET':
        type_array = ['', 'hot', 'young', 'relax', '', '', '1', '2', '3', '4', '5']
        return_array = slug.split('-')
        schedule_search = []
        content = {}
        show_array = []
        for chose_option in return_array:
            if int(chose_option) <= 3:
                search_tem = Schedule.objects.filter(style=type_array[int(chose_option)])
                for sc in search_tem:
                    if sc.id in schedule_search:
                        continue
                    else:
                        schedule_search.append(sc.id)
            else:
                search_tem = Schedule.objects.filter(days=type_array[int(chose_option)])
                for sc in search_tem:
                    if sc.id in schedule_search:
                        continue
                    else:
                        schedule_search.append(sc.id)

        schedule_search.sort()
        print(schedule_search)
        for sch_id in schedule_search:
            show_array.append(Schedule.objects.get(id=sch_id).image)
        content['show_array'] = show_array
        print(show_array)
        return render(request,'show.html',content)


def sch(request,id_num):
    schedule_now = Schedule.objects.get(id=id_num)
    schedule_all_course= schedule_now.totalcourse_set.all()
    max_day = schedule_all_course.aggregate(Max('day'))['day__max']
    content={}
    if request.method == 'GET':
        content['max_day'] = max_day
        schedule_all_course_by_day = []
        for i in range(max_day):
            course_tem=schedule_all_course.get(day=i + 1).touristsite_set.all()
            schedule_all_course_by_day.append(course_tem)
        content['site_information'] = schedule_all_course_by_day
        #print(content['site_information'])
        first_day_site = schedule_all_course.get(day=1).touristsite_set.all()
        if first_day_site.count() !=0:
            content['origin'] = first_day_site.get(route_order = 0).location
        if first_day_site.count() > 1:
            content['destination'] = first_day_site.get(route_order = first_day_site.count()-1).location
        content['waypoints'] = []
        if first_day_site.count()>2:
            for i in range(1, first_day_site.count()-1):
                print(i)
                content['waypoints'].append(first_day_site.get(route_order= i).location)
        content['first_time_load']=1
        return render_to_response('sch.html',content)
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
            if len(order) >0:
                content['origin'] = {'placeId': TouristSite.objects.get(site_id=order[0]).location}
            if len(order) > 1:
                content['destination'] = {'placeId': TouristSite.objects.get(site_id=order[len(order) - 1]).location}
            content['waypoints'] = []
            for i in range(1, len(order) - 1):
                print(i)
                content['waypoints'].append({'stopover': True, 'location': {'placeId':TouristSite.objects.get(site_id=order[i]).location}})
            return JsonResponse(content)
        elif request.POST.get('type','') == 'change_day_init':
            day_cur = request.POST.get('day_cur', '')
            first_day_site = schedule_all_course.get(day=day_cur).touristsite_set.all()
            if first_day_site.count() != 0:
                content['origin'] = {'placeId': first_day_site.get(route_order=0).location}
            if first_day_site.count() > 1:
                content['destination'] = {'placeId': first_day_site.get(route_order=first_day_site.count()-1).location}
            content['waypoints'] = []
            if first_day_site.count() > 2:
                for i in range(1, first_day_site.count()-1):
                    print(i)
                    content['waypoints'].append({'stopover': True, 'location': {'placeId':first_day_site.get(route_order=i).location}})
            return JsonResponse(content)
        elif request.POST.get('type','') == 'add_site':

            place_name=request.POST.get('site_name','')
            place_id = search(request.POST.get('site_name',''))
            place_phone = detail(place_id)['phone_number']
            place_address = detail(place_id)['address']
            camera(place_id,place_name)
            day_cur=request.POST.get('day_cur','')
            schedule_all_course_now = schedule_now.totalcourse_set.all().get(day=day_cur)
            site_num = TouristSite.objects.all().aggregate(Max('site_id'))['site_id__max']+1
            try:
                site_route_order = schedule_all_course_now.touristsite_set.all().aggregate(Max('route_order'))['route_order__max']+1
            except:
                site_route_order = 0
            new_site= TouristSite.objects.create(route_order = site_route_order , address = place_address , phone_number = place_phone, \
            site_name=place_name, image="/media/image/"+place_name+".jpg", location=place_id ,\
            site_content="", site_id = site_num , line_id = schedule_all_course_now.id)
            image_url="/media/image/"+place_name+".jpg"
            content['site_id'] = site_num
            content['image_url'] = image_url
            content['site_name'] = place_name
            content['route_order'] = site_route_order
            content['line_id'] = schedule_all_course_now.id
            content['phone'] = place_phone
            content['address'] = place_address
            return JsonResponse(content)
        elif request.POST.get('type','') == 'add_day':
            schedule_now.days+=1
            schedule_now.save()
            content['day_num'] = int(max_day)+1
            new_totalcourse = TotalCourse.objects.create(day=content['day_num'], course_id = id_num)
            return JsonResponse(content)
        elif request.POST.get('type','') == 'delete_site':
            delete_site = TouristSite.objects.get(site_id=request.POST.get('site_id',''))
            route_order = delete_site.route_order
            delete_line_id = delete_site.line
            to_order_site = TotalCourse.objects.get(id=str(delete_line_id)).touristsite_set.filter(route_order__gt=route_order)
            for site_to_order in to_order_site:
                site_to_order.route_order -= 1
                site_to_order.save()
            delete_site.delete()
            return JsonResponse(content)
        elif request.POST.get('type', '') == 'update_content':
            update_site = TouristSite.objects.get(site_id=request.POST.get('site_id', ''))
            update_site.site_content = request.POST.get('site_content','')
            update_site.save()
            return JsonResponse(content)
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
        result['phone_number'] = ' '
    try:
        result['address'] = result_json['result']['formatted_address']
    except:
        result['address'] = ' '

    return result

def camera(place_id,site_name):
    url_temp = ("https://maps.googleapis.com/maps/api/place/details/json?" +
                "placeid=" + place_id +
                "&key=" + "AIzaSyB2pGT9ePkt26BbSk1tvcPWXg1_8ZZ8lM8" +
                '')
    res = requests.get(url_temp)
    result = json.loads(res.content.decode('utf-8'))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    fo = open('detail.json', 'w', encoding="utf-8")
    fo.write(json.dumps(result, ensure_ascii=False, indent=2))
    photo_reference = result['result']['photos'][0]['photo_reference']

    url_temp = ('https://maps.googleapis.com/maps/api/place/photo?' +
                'key=' + 'AIzaSyB2pGT9ePkt26BbSk1tvcPWXg1_8ZZ8lM8' +
                '&photoreference=' + photo_reference +
                '&maxwidth=' + '600')

    res = requests.get(url_temp)
    content = BytesIO(res.content)
    file = open('./media/image/'+site_name+'.jpg', 'wb+')
    file.write(content.read())
    file.close()

    return True

