from __future__ import unicode_literals
# Create your views here.
from django.shortcuts import render, redirect,render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from .models import TouristSite,IMG,Schedule,TotalCourse
from django.http import JsonResponse
import json,re
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.http import JsonResponse

def aaa(request):
        return render(request, 'aaa.html')

def sch(request):
    s = Schedule.objects.all()
    tc = TotalCourse.objects.all();
    tc0 = TotalCourse.objects.get(day = 0)
    tc1 = TotalCourse.objects.get(day = 1)
    tc2 = TotalCourse.objects.get(day = 2)
    tc3 = TotalCourse.objects.get(day = 3)
    
    if 'ok' in request.POST:
        site_name = request.POST['site_name']
        time = request.POST['time']
        a = int(request.POST['whichday'])
        tcc = TotalCourse.objects.get(day = a)
        TouristSite.objects.create(route_order =tcc.touristsite_set.count()+1,site_name = site_name, time = time, line = tcc)
    #reorder use sortable and re
    if 'order' in request.POST:
        course = request.POST['course']
        order = request.POST['order0']
        newOrder = re.findall(r'[0-9]+',order)
        i=0
        while(i<len(newOrder)): 
            try:
                temp = TouristSite.objects.get(site_id = newOrder[i])
                TouristSite.objects.get(site_id = newOrder[i])
                temp = TouristSite.objects.get(site_id = newOrder[i])
                if(temp.line != tc0):
                    temp.line = tc0
                temp.route_order = i
                temp.save()
                i+=1
            except:
                i = len(newOrder)+1
        order = request.POST['order1']
        newOrder = re.findall(r'[0-9]+',order)
        i=0
        while(i<len(newOrder)): 
            try:
                temp = TouristSite.objects.get(site_id = newOrder[i])
                if(temp.line != tc1):
                    temp.line = tc1
                temp.route_order = i
                temp.save()
                i+=1
            except:
                i = len(newOrder)+1
    return render_to_response('ns.html',locals())
    #reorder use draggable and index
"""
    ptr = 0
    
    if 'order' in request.POST:
        order = request.POST['order']
        pos = order.find('>', ptr)
        while(pos>0):  
            old = int(order[pos-1])
            new = int(order[pos+1])
            temp = TouristSite.objects.get(route_order = old) 
            temp.route_order = new
            if old > new:
                for i in range(old-1, new-1, -1):
                    a = TouristSite.objects.get(route_order = i)
                    a.route_order += 1
                    a.save()
            elif old < new:
                for j in range(old+1,new+1):
                    b = TouristSite.objects.get(route_order = j)
                    b.route_order-=1
                    b.save()
            temp.save()
            ptr = pos+1
            pos = order.find('>', ptr)

    return render_to_response('ns.html',locals())
"""
def query(request):
    r=request.GET.get("toolsname")
    name_dict="123"
    return JsonResponse(name_dict)
# Create your views here.
def form(request):
    return render_to_response('form.html',locals())
def ind(request):
    return render(request,'index.html')
def drag(request):
    return render_to_response('drag.html',locals())
def uploadImg(request):
    if request.method == 'POST':
        new_img = IMG(img=request.FILES.get('img'))
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


def addNewScheduleToDatabase(content):
    obj = Schedule.objects.create(title=content['title'],author=content['author'],days=content['days'],
                location=content['location'],course_content=content['course_content'])
    return obj

def addNewLineToDatabase(content):
    obj = TotalLines.objects.create(title=content['day'],site_content=content['site_content'],Course=content['pk'])
    
    return obj


def schedule(request):
    content = {}
    if request.method == 'GET':
        day_1_all = Schedule_content.objects.all()
        content['day_1_all'] = day_1_all
        print(content['day_1_all'])
        print("adad")
        return render(request, 'schedule.html', content)

    if request.method == 'POST':
        day_1_all = Schedule_content.objects.all()
        content['day_1_all'] = day_1_all
        content['day']=int(request.POST['whichday'][4:])
        content['seq']=request.POST['seq']
        content['title'] = request.POST['title']
        # content['pk'] = request.POST['pk']#need to be added by html or javascript
        # newLine = addNewLineToDatabase(content)
        sites = []
        i = 0
        # print(sites)
        f = Schedule_content(day=content['day'], seq=content['seq'], title=content['title'])
        f.save()
        #content['pk'] = 6
        return render(request, 'schedule.html', content)

def login(request):
    if request.user.is_authenticated :
        return HttpResponRedirect('/schedule')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username = username, password = password)

    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/schedule')
    else:
        return render_to_response('login.html') 
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/schedule')

def register(request):
    if request.method =="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/accounts/login/')
    else:
        form = UserCreationForm()
    return render_to_response('register.html',locals())
