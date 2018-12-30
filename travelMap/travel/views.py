from __future__ import unicode_literals
# Create your views here.
import json
# import requests
import re
from django.shortcuts import render, render_to_response,redirect
from .models import TouristSite, IMG, Schedule, TotalCourse,MapSite
from django.db.models import Max
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect,HttpResponseNotFound
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import random
import requests
from PIL import Image
from jieba_space import jieba_test
from django.contrib.auth.decorators import login_required
from io import BytesIO


def develop(request):
    if request.method == 'GET':
        schedule_idset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        random.shuffle(schedule_idset)
        schedule_item = list()
        for i in range(0, len(schedule_idset)):
            schedule_item.append(Schedule())
            schedule_item[i] = Schedule.objects.get(id_num=schedule_idset[i])
        content = {}
        content['schedule_item'] = schedule_item
        content['user'] = request.user
        return render_to_response('develop.html',  content)


def search_dis(request):
    if request.method =='GET':
        content = {}
        content['user'] = request.user
        return render_to_response('search.html',content)


@login_required(login_url='/accounts/login/')
def show(request,slug):
    print('in')
    print(slug)
    content={}
    content['user'] = request.user
    if request.method == 'GET':
        type_array = ['', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        return_array = slug.split('-')
        for indx,opt in enumerate(return_array):
            return_array[indx] = type_array[int(opt)]
        schedule_search = []
        content = {}
        show_array = []
        sch_all = Schedule.objects.all()
        for chose_option in return_array:
            for each_sch in sch_all:
                each_sch_style = []
                each_sch_style = each_sch.style.split(',')
                if chose_option in each_sch_style:
                    if each_sch.id in schedule_search:
                        continue
                    else:
                        schedule_search.append(each_sch.id)
        schedule_search.sort()
        print(schedule_search)
        for sch_id in schedule_search:
            show_array.append(Schedule.objects.get(id=sch_id).image)
        content['show_array'] = show_array
        print(show_array)
        return render(request,'show.html',content)


@login_required(login_url='/accounts/login/')
def sch(request,id_num):
    if id_num == 0:
        new_schedule = Schedule.objects.all().aggregate(Max('id'))['id__max'] + 1
        return HttpResponseRedirect("../sch/"+str(new_schedule))
    try:
        content={}
        schedule_now = Schedule.objects.get(id=id_num)
        check=1
    except:
        check=0
    if check ==1:
        if int(request.user.id) == int(schedule_now.author):
            schedule_all_course= schedule_now.totalcourse_set.all()
            if schedule_all_course.count() == 0:
                max_day=0
            else:
                max_day = schedule_all_course.aggregate(Max('day'))['day__max']
            content['schedule_title'] = schedule_now.title
            content['schedule_content'] = schedule_now.content
            content['create'] = 0
            if request.method == 'GET':
                content['max_day'] = max_day
                schedule_all_course_by_day = []
                for i in range(max_day):
                    course_tem=schedule_all_course.get(day=i + 1).touristsite_set.all()
                    schedule_all_course_by_day.append(course_tem)
                content['site_information'] = schedule_all_course_by_day
                #print(content['site_information'])
                try:
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
                except:
                    print('no first day')
                content['user'] = request.user
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
                elif request.POST.get('type', '') == 'create_schedule':
                    schedule_now.title = request.POST.get('schedule_name','')
                    schedule_now.content = request.POST.get('schedule_content','')
                    schedule_now.save()
                    result = jieba_test.find_sites(request.POST.get('jieba_input_result',''))
                    print(result)
                    if len(result) !=0:
                        result = decide_course(result)
                        print(result)
                        for ind,day_course in enumerate(result):
                            for create_site in day_course:
                                place_name = create_site['name']
                                print(type(place_name))
                                place_id = search(place_name)
                                place_phone = detail(place_id)['phone_number']
                                place_address = detail(place_id)['address']
                                camera(place_id, place_name)
                                day_cur = ind+1
                                try:
                                    schedule_all_course_now = schedule_now.totalcourse_set.all().get(day=day_cur)
                                except:
                                    TotalCourse.objects.create(day=day_cur, course_id= id_num)
                                    schedule_all_course_now = schedule_now.totalcourse_set.all().get(day=day_cur)
                                site_num = TouristSite.objects.all().aggregate(Max('site_id'))['site_id__max'] + 1
                                try:
                                    site_route_order = \
                                    schedule_all_course_now.touristsite_set.all().aggregate(Max('route_order'))[
                                        'route_order__max'] + 1
                                except:
                                    site_route_order = 0
                                new_site = TouristSite.objects.create(route_order=site_route_order, address=place_address,
                                                                      phone_number=place_phone, \
                                                                      site_name=place_name,
                                                                      image="/media/image/" + place_name + ".jpg",
                                                                      location=place_id, \
                                                                      site_content="", site_id=site_num,
                                                                      line_id=schedule_all_course_now.id)
                    content['max_day'] = max_day
                    schedule_all_course_by_day = []
                    for i in range(max_day):
                        course_tem = schedule_all_course.get(day=i + 1).touristsite_set.all()
                        schedule_all_course_by_day.append(course_tem)
                    content['site_information'] = schedule_all_course_by_day
                    # print(content['site_information'])
                    return JsonResponse(content)
        else:
            print(request.user.id)
            return HttpResponseRedirect("../develop/")
    else:
        print('not exist')
        create_schedule = Schedule.objects.create(id=id_num, id_num=id_num, author=request.user.id, days=0, title="未命名")
        content['max_day'] = 0
        content['site_information'] = []
        content['create']=1
        content['first_time_load'] = 0
        return render_to_response('sch.html', content)


def extract_article(request):#extract article to list tourist sites
    if request.method == 'POST':
        sentence = request.POST['article']
        result = jieba_test.find_sites(sentence)
        #result = ["藍晒圖文創園區","321巷 藝術聚落","銀同社區貓咪高地","蝸牛巷","巨大扭蛋機","神農街","原鶯料理","綠芝屋意麵","暖暖蛇"]
        result = decide_course(result)
        print(result)
        #修改看要render到哪裡
        return render(request,'result.html',locals())
    return render(request,'extract.html')


def search(name):
    print('search')
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
    print(list(result))
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


''''''''

result = []
site_result= {}


def show_result(request):
    results = result
    render(request,'result.html',locals())


'''''''''user sytem'''''''''


def login(request):
    print('login')
    if request.user.is_authenticated :
        return HttpResponseRedirect('/develop')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username = username, password = password)

    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/develop')
    else:
        return render_to_response('login.html'  )


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/develop')


def register(request):#在register.html頁面我有稍微美化一下
    if request.method =="POST":
        form = UserCreationForm(request.POST)
        '''
        <form action="" method="post">
		<p><label for="id_username">Username:</label> 
        <input type="text" name="username" maxlength="150" autofocus required id="id_username"> 
        <span class="helptext">Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</span></p>
        <p><label for="id_password1">Password:</label> <input type="password" name="password1" required id="id_password1"></p>
        <p><label for="id_password2">Password confirmation:</label> <input type="password" name="password2" required id="id_password2"> <span class="helptext">Enter the same password as before, for verification.</span></p>
		<input type="submit" value="註冊">
	    </form>
        '''
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/accounts/login/')
    else:
        form = UserCreationForm()
    return render_to_response('register.html',locals())


'''''''''''''''''''''''新的function'''''''''''''''''''''


def decide_course(original_course):
    result = []
    site = []
    food = []
    new_site = []
    adjust_course = [[]]
    adjust_course_day = []
    result = []
    small_result = []
    day = 0
    '''
    with open('site_info.json', 'r', encoding='utf-8') as f:
        json_dict = json.loads(f.read(),encoding="utf-8")
        for dic in json_dict:
            if dic["sort"]=="site":
                site.append(dic["name"])
            elif dic["sort"]=="food":
                food.append(dic["name"])
        #print (site)
    '''
    # 把景點作2分法
    for item in original_course:
        m = MapSite.objects.filter(name__contains=item)

        if (m[0]):
            if (len(m[0].site_type) == 1):
                if (m[0].site_type == 'j'):
                    food.append(m[0])
            else:
                token = m[0].site_type.split(',')
                for i in token:
                    if (i == 'j'):  # type =food
                        food.append(m[0])
                        break
                else:
                    site.append(m[0])

    # 生產行程
    i = 0
    j = 0
    number = 0
    print(site)
    print(food)

    while (i < site.__len__() or j < food.__len__()):
        print('i=', i, 'j=', j)
        if (i >= len(site)):
            for jj in range(j, len(food)):
                adjust_course[day].append(food[jj])
                print(food[jj])
            break
        else:
            adjust_course[day].append(site[i])
            print(site[i])
        i += 1
        number += 1
        if (number % 2 == 0):
            if (j < food.__len__()):
                adjust_course[day].append(food[j])
                print(food[j])
                j += 1
                if (j % 2 == 0):
                    adjust_course.append(adjust_course_day)  # 2個food就換成下一天
                    print(adjust_course)
                    day += 1
                    number = 0
            else:
                for ii in range(i, len(site)):
                    adjust_course[day].append(site[ii])
                break

    print(adjust_course)
    for item in adjust_course:
        for inner_item in item:
            # small_result可再增加需要回傳的資訊
            small_result.append({
                'name': inner_item.name,
                'location': inner_item.location,
                'phone number': inner_item.phone_number,
                'address': inner_item.address
            })
        result.append(small_result)
    # print(result)

    # result形式上會是[ [...], [...], [...], [...]...   ]
    # 每一個inner list 都代表一天

    return result


# 接前端
def filter_(request):
    filter_schedule(['a', 'g'])
    return render(request, 'filter.html')


'''''''''''''''新的function'''''''''''''''''


# input_list 接[a,b,c,d...]
def filter_schedule(input_list):
    all_objects = Schedule.objects.all()
    choosable_list = []
    flag = True
    for item in all_objects:
        style = item.style
        if (len(style) > 1):
            token = style.split(',')
            for i in input_list:
                for j in token:
                    if (i == j):
                        choosable_list.append(item.name)
                        flag = False
                        break
                if (flag == False):
                    break
            flag = True
        else:
            for i in input_list:
                if (i == style):
                    choosable_list.append(item.name)
                    break

    # return schedule裡的name
    return choosable_list


def display(request, input_day):
    if request.method == 'GET':
        if input_day == "":
            input_day = 1
            # return render(request, "display.html")
        else:
            input_day = input_day
        # return HttpResponseNotFound("<h>%s</h>" % [day, ])
        try:
            single_schedule = Schedule.objects.get(pk=int(input_day))
        except:
            return HttpResponseNotFound('No such schedule')
        total_result = {}
        if not single_schedule:
            return HttpResponseNotFound("No such schedule.")
        days = single_schedule.id_num
        days_content = TotalCourse.objects.filter(course_id=input_day)

        total_result['total_day'] = single_schedule.days
        total_result['img'] = single_schedule.image
        total_result['content'] = single_schedule.content
        total_result['days_schedule'] = []
        total_result['random_color'] = []
        total_result['first_time_load']=1
        for day in days_content:
            sites = TouristSite.objects.filter(line_id=day.id)
            total_result['days_schedule'].append(sites)
        # logging.error(total_result['days_schedule'])
        '''chang'''
        schedule_all_course = single_schedule.totalcourse_set.all()
        if schedule_all_course.count() == 0:
            max_day = 0
        else:
            max_day = schedule_all_course.aggregate(Max('day'))['day__max']
            total_result['max_day'] = max_day
            try:
                first_day_site = schedule_all_course.get(day=1).touristsite_set.all()
                if first_day_site.count() != 0:
                    total_result['origin'] = first_day_site.get(route_order=0).location
                if first_day_site.count() > 1:
                    total_result['destination'] = first_day_site.get(route_order=first_day_site.count() - 1).location
                total_result['waypoints'] = []
                if first_day_site.count() > 2:
                    for i in range(1, first_day_site.count() - 1):
                        print(i)
                        total_result['waypoints'].append(first_day_site.get(route_order=i).location)
            except:
                print('no first day')
        return render(request, "display.html", total_result)
    elif request.method == 'POST':
        content = {}
        schedule_now = Schedule.objects.get(id=input_day)
        schedule_all_course = schedule_now.totalcourse_set.all()
        day_cur = request.POST.get('day_cur', '')
        first_day_site = schedule_all_course.get(day=day_cur).touristsite_set.all()
        if first_day_site.count() != 0:
            content['origin'] = {'placeId': first_day_site.get(route_order=0).location}
        if first_day_site.count() > 1:
            content['destination'] = {'placeId': first_day_site.get(route_order=first_day_site.count() - 1).location}
        content['waypoints'] = []
        if first_day_site.count() > 2:
            for i in range(1, first_day_site.count() - 1):
                print(i)
                content['waypoints'].append(
                    {'stopover': True, 'location': {'placeId': first_day_site.get(route_order=i).location}})
        return JsonResponse(content)

