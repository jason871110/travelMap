from __future__ import unicode_literals
# Create your views here.
import json
#import requests
import json,re
from django.shortcuts import render, redirect,render_to_response
from django.urls import reverse
from django.template import RequestContext
from .models import TouristSite, IMG, Schedule, TotalCourse
from django.db.models import Max
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Count
from jieba_space import jieba_test
import static
import json
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django import forms
import random
def develop(request):
  
    schedule_idset = [1,2,3,4,5,6,7,8,9,10]
    random.shuffle(schedule_idset)
    schedule_item = list()
    for i in range(0,len(schedule_idset)):
        schedule_item.append(Schedule())   
        schedule_item[i] = Schedule.objects.get(id_num=schedule_idset[i])
        
    return render_to_response('develop.html',{'schedule_item':schedule_item}) 

class siteForm(forms.ModelForm):
    class Meta:
        model = TouristSite
        fields = ['site_name','site_content', 'time', 'line']

def create_form(request):
    if request.method == 'POST':
        form = siteForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            tcc = data['line']
            TouristSite.objects.create(route_order =tcc.touristsite_set.count()+1,site_id=TouristSite.objects.all().count()+1,site_name = data['site_name'], time = data['time'], site_content=data['site_content'],line = tcc)
            if request.user.is_authenticated:
                print(request.user.username)
            #print(data['line'])
            #form.save()
            return HttpResponseRedirect('compre_form.html')

    form = siteForm()
    return render(request, 'compre_form.html', {'form': form})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/form')

def login(request):

    if request.user.is_authenticated: 
        return HttpResponseRedirect('/form')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    
    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('form.html')
    else:
        return render_to_response('login.html') 
def home(request):
    return render_to_response('home.html',locals()) 
def register(request):
    if request.method =="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/accounts/login/')
    else:
        form = UserCreationForm()
    return render_to_response('register.html',locals())

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



def extract_article(request):#extract article to list tourist sites
    if request.method == 'POST':
        sentence = request.POST['article']
        result = jieba_test.find_sites(sentence)
        #print(result)
        return render(request,'result.html',locals())
    return render(request,'extract.html')
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
def form(request):
    if 'ok' in request.POST:
        site_name = request.POST['site_name']
        time = request.POST['time']
        a = int(request.POST['whichday'])
        tcc = TotalCourse.objects.get(day = a)
        TouristSite.objects.create(route_order =tcc.touristsite_set.count()+1,site_id=TouristSite.objects.all().count()+1,site_name = site_name, time = time, line = tcc)
    return render_to_response('form.html',locals())

def addNewScheduleToDatabase(content):
    obj = Schedule.objects.create(title=content['title'], author=content['author'], days=content['days'],
                                  location=content['location'], course_content=content['course_content'])
    return obj


def addNewLineToDatabase(content):
    obj = TotalCourse.objects.create(title=content['day'],site_content=content['site_content'],Course=content['pk'])
    
    return obj


def main(request, id_num):
    content={}
    if request.method == 'GET':
        schedule_all = Schedule.objects.get(id_num=id_num)
        schedule_day_all = schedule_all.totalcourse_set.all()
        #print(schedule_all.days)
        num_of_day = [0]*(schedule_all.days+1)

        for sche in schedule_day_all:
            for site in sche.touristsite_set.all():
                num_of_day[sche.day] += 1

        content['schedule_title'] = schedule_all.title
        content['schedule_day_all'] = schedule_day_all
        content['max_day'] = schedule_all.days
        content['num_of_day'] = num_of_day
        #print(schedule_day_all.get(day=1).touristsite_set.all().get(route_order=0).location)
        content['origin'] = schedule_day_all.get(day=1).touristsite_set.all().get(route_order=0).location
        content['destination'] = schedule_day_all.get(day=1).touristsite_set.all().get(route_order=num_of_day[1]-1).location
        content['waypoints'] = []
        for i in range(2,num_of_day[1]):
            content['waypoints'].append(schedule_day_all.get(day=1).touristsite_set.all().get(route_order=i).location)
        #print(content['origin']+"%%%from get")
        return render(request, 'main.html', content)
    elif request.method == 'POST':
        target_day = request.POST['day']
        schedule_all = Schedule.objects.get(id_num=id_num)
        schedule_day_all = schedule_all.totalcourse_set.all()
        print(schedule_all.days)
        num_of_day = [0] * (schedule_all.days + 1)
        content['img_site'] = []
        for sche in schedule_day_all:
            for site in sche.touristsite_set.all():
                num_of_day[sche.day] += 1
                content['img_site'].append(site.image)
                print(site.image)
        #print(content['img_site'])

        content['schedule_day_all'] = schedule_day_all
        content['max_day'] = schedule_all.days
        content['num_of_day'] = num_of_day
        content['origin'] = schedule_day_all.get(day=target_day).touristsite_set.all().get(route_order = 0).location
        content['destination'] = schedule_day_all.get(day=target_day).touristsite_set.all().get(route_order=num_of_day[int(target_day)]-1).location
        content['waypoints'] = []
        for i in range(2, num_of_day[int(target_day)]):
            content['waypoints'].append(schedule_day_all.get(day=target_day).touristsite_set.all().get(route_order=i).location)
        #print(content['origin']+'%%%from post')
        return render(request,'main.html',content)
        #return render_to_response('main.html', content,context_instance = RequestContext(request))
        #return HttpResponseRedirect(reverse('main',kwargs={'id_num':0}))
    return render(request, 'main.html')


def search(name):
    if not (type(name) is str):
        raise ValueError("Should be string")
    fo = open('total_results.json', encoding='utf-8')
    json_dict = json.loads(fo.read())
    for key, value in json_dict.items():
        if key.find(name) != -1:
            print(key)
            return value
    fo.close()
    url_temp = ("https://maps.googleapis.com/maps/api/place/findplacefromtext/json?" +
                "input=" + name +
                "&key=" + "AIzaSyCS54PJ0zmirq0QNN29mKfPaJVE0KDCiTc" +
                "&inputtype=" + "textquery" +
                "&locationbias=" + "ipbias")
    res = requests.get(url_temp)
    # print(res)
    # print(type(res.content))
    # print(str(res.content))

    result = res.content.decode("utf-8")
    result = json.loads(result)
    print(list(result))
    if (len(result["candidates"]) == 0):
        return None
    result_id = result['candidates'][0]["place_id"]
    result_name = name
    fo = open('total_results.json', 'r+', encoding='utf-8')

    file_str = fo.read()
    file_json = json.loads(file_str)
    file_json[result_name] = result_id
    fo.write(json.dumps(file_json, ensure_ascii=False, indent=2))
    fo.close()
    return result_id


def sch(request):
    s = Schedule.objects.all()
    tc = TotalCourse.objects.all();
    tc0 = TotalCourse.objects.get(day=0)
    tc1 = TotalCourse.objects.get(day=1)
    content={}
    if request.method == "GET":
        print('get')
        content['tc'] = tc
        content['tc0'] = tc0
        content['tc1'] = tc1
        schedule_all = Schedule.objects.get(id_num=0)
        schedule_day_all = schedule_all.totalcourse_set.all()
        num_of_day = [0] * (schedule_all.days + 1)

        for sche in schedule_day_all:
            for site in sche.touristsite_set.all():
                num_of_day[sche.day] += 1
        content['origin'] = schedule_day_all.get(day=1).touristsite_set.all().get(route_order=0).location
        content['destination'] = schedule_day_all.get(day=1).touristsite_set.all().get(
            route_order=num_of_day[1] - 1).location
        content['waypoints'] = []
        for i in range(1, num_of_day[1]-1):
            content['waypoints'].append(schedule_day_all.get(day=1).touristsite_set.all().get(route_order=i).location)
        #print(content)
        render(request,'ns.html',content)

    if request.method =="POST":
        print('in')
        content['tc']=tc
        content['tc0']=tc0
        content['tc1']=tc1
        schedule_all = Schedule.objects.get(id_num=0)
        schedule_day_all = schedule_all.totalcourse_set.all()
        num_of_day = [0] * (schedule_all.days + 1)

        for sche in schedule_day_all:
            for site in sche.touristsite_set.all():
                num_of_day[sche.day] += 1


        # reorder use sortable and re
        #if 'order' in request.POST:
       #print('inorder')
        #course = request.POST['course']
        order = request.POST.get('order0','')
        newOrder = re.findall(r'[0-9]+', order)
        i = 0
        while (i < len(newOrder)):
            try:
                temp = TouristSite.objects.get(site_id=newOrder[i])
                TouristSite.objects.get(site_id=newOrder[i])
                temp = TouristSite.objects.get(site_id=newOrder[i])
                if (temp.line != tc0):
                    temp.line = tc0
                temp.route_order = i
                temp.save()
                i += 1
            except:
                i = len(newOrder) + 1
        order = request.POST.get('order1','')
        newOrder = re.findall(r'[0-9]+', order)
        i = 0
        while (i < len(newOrder)):
            try:
                temp = TouristSite.objects.get(site_id=newOrder[i])
                if (temp.line != tc1):
                    temp.line = tc1
                temp.route_order = i
                temp.save()
                i += 1
            except:
                i = len(newOrder) + 1
        '''
        else:
            if 'ok' in request.POST:
                site_name = request.POST['site_name']
                time = request.POST['time']
                a = int(request.POST['whichday'])
                tcc = TotalCourse.objects.get(day=a)
                TouristSite.objects.create(route_order=tcc.touristsite_set.count() + 1, site_name=site_name, time=time,
                                           line=tcc)
        '''
        content['origin'] = TouristSite.objects.get(site_id=newOrder[0]).location
        content['destination'] = TouristSite.objects.get(site_id=newOrder[len(newOrder)-1]).location
        content['waypoints'] = []
        for i in range(1, len(newOrder)-1):
            #print(newOrder[i])
            content['waypoints'].append(TouristSite.objects.get(site_id=newOrder[i]).location)


        return render(request,'ns.html',content)

    return render_to_response('ns.html', content)
    # reorder use draggable and index