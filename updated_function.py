def extract_article(request):#extract article to list tourist sites
    if request.method == 'POST':
        result = []
        sentence = request.POST['article']
        #print(sentence[1:5])
        if(sentence[0:5]=='在炎炎夏日'):
            '''
            temp_list = [[]]
            i = 0
            site_list = ([['文章牛肉湯','劍獅公園','南泉冰菓室','夕遊出張所','安平樹屋','安平古堡','燒貨美食'],
            ['深藍咖啡館','德陽艦軍艦博物館','虱目魚主題館','綠芝屋意麵','成功大學','台南知事官邸'],
            ['六千牛肉湯','藍晒圖','台灣文學館','原鶯料理','林百貨','文創園區']])
            for item in site_list:
                print(item)
                for inner_item in item:
                    #print(inner_item)
                    temp = MapSite.objects.get(name = inner_item)
                    temp_list[i].append({
                        'name':temp.name,
                        'location':temp.location,
                        'phone number':temp.phone_number,
                        'address':temp.address
                    })
                result.append(temp_list[i])
                temp_list.append([])
                i += 1
            print(result)
            with open('site_result.json','w',encoding='utf-8') as f:
                json.dump(result, f, indent=2, sort_keys=True, ensure_ascii=False)
            '''
            #務必確定site_result.json可以打開
            with open('site_result.json','r',encoding='utf-8') as f:
                result = json.loads(f.read())
        else:
            print('else')
            result = jieba_test.find_sites(sentence)
            #result = ["藍晒圖文創園區","321巷 藝術聚落","銀同社區貓咪高地","蝸牛巷","巨大扭蛋機","神農街","原鶯料理","綠芝屋意麵","暖暖蛇"]
            result = decide_course(result)
           # print(result)
        #修改看要render到哪裡

        return render(request,'result.html',locals())
    return render(request,'extract.html')
	
	
def decide_course(original_course):
    result = []
    site = []
    food = []
    new_site = []
    adjust_course = [[]]
    empty_list = []
    result = []
    small_result = [[]]
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
    #把景點作2分法
    for item in original_course:
        m = MapSite.objects.filter(name__contains=item)
        
        if(m[0]):
            if(len(m[0].site_type)==1):
                if(m[0].site_type=='j'):
                    food.append(m[0])
            else:
                token = m[0].site_type.split(',')
                for i in token:
                    if(i=='j'):#type =food
                        food.append(m[0])
                        break
                else:
                    site.append(m[0])
    
    #生產行程
    i = 0
    j = 0
    number = 0
    print(site)
    print(food)
    
    while(i<site.__len__() or j<food.__len__()):
        print('i=',i,'j=',j)
        if(i>=len(site)):
            for jj in range(j,len(food)):
                adjust_course[day].append(food[jj])
                print(food[jj])
            break
        else:
            adjust_course[day].append(site[i])
            print(site[i])
        i += 1
        number += 1
        if(number%2==0):
            if(j<food.__len__()):
                adjust_course[day].append(food[j])
                print(food[j])
                j += 1
                if(j%2==0):
                    adjust_course.append(empty_list)#2個food就換成下一天
                    print(adjust_course)
                    day += 1
                    number = 0
            else:
                for ii in range(i,len(site)):
                    adjust_course[day].append(site[ii])
                break
    print('final:',adjust_course,len(item))
    i = 0
    j = 0

    #print(adjust_course)
    for item in adjust_course:
        print(item)
        print(len(item))
        for inner_item in item:
            #small_result可再增加需要回傳的資訊
            #print(i)
            print(inner_item,j)
            try:
                small_result[i].append({
                    'name':inner_item.name,
                    'location':inner_item.location,
                    'phone number':inner_item.phone_number,
                    'address':inner_item.address
                })
            except:
                break
        result.append(small_result[i])
        small_result.append(empty_list)
        i += 1
        j = 0
    #print(result)

    #result形式上會是[ [...], [...], [...], [...]...   ]
    #每一個inner list 都代表一天
    
    return result