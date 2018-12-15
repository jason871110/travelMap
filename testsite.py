import json
#from bs4 import BeautifulSoup
import requests
import re
from PIL import Image
from io import BytesIO
from travel.models import MapSite
from django.core.files import File
def decide_course(original_course):
    result = []
    result.append([])
    result.append([])
    adjust_course = []
    bool_table = []
    schedule = 0
    with open('site_info.json', 'r', encoding='utf-8') as f:
        json_dict = json.loads(f.read(),encoding="utf-8")
        

        number = 1
        for item in original_course:
            for dic in json_dict:
                if item == dic['name']:
                    adjust_course.append(dic)
                    break
            else:#give default value
                adjust_course.append(
                    {
                        "name":item,
                        "sort":"site",
                        "location":123456,
                        "stay":60
                    }
                )
        #print(adjust_course)
        
        for item in adjust_course:
            if item['sort']=='site':
                result[schedule].append(item['name'])
                number = number + 1
            if number%5 == 0:
                number = 1
                schedule = schedule + 1

        if number!=1:
            schedule = schedule + 1
        counter  = 2
        flag = False
        for item in adjust_course:
            for i in range(schedule):
                if item['sort'] == 'food':
                    result[i].insert(counter, item['name'])
                    flag = True
            if flag:
                counter = counter + 3
                flag = False
        print(result)       
        print(len(adjust_course))

    return result


def searchStay(site):
    #url_temp = "https://www.google.com.tw/search?ei=3ZIMXNeNHceY8gWPk41I&q=" + site
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    total_content = []
    for i in site:
        url_temp = 'https://www.google.com.tw/search?q='+i
        res = requests.get(url=url_temp,headers=headers)
        soup = BeautifulSoup(res.text,'html.parser')
        row_data = soup.find('div','UYKlhc')
        if row_data:
            #print(row_data)
            string1 = list(row_data.contents)
            #print(string1[1])
            time = str(string1[1])
            reg = re.compile('<[^>]*>')
            content = reg.sub('',time).replace('\n','').replace(' ','')
            total_content.append({i:content})
            print(i,':',content)
        for j in range(100000):
            j = 1
    with open('time.txt','w') as f:
        f.write(str(total_content))
    #with open('result.txt','w',encoding="utf-8") as f:
     #   f.write(res.text)


def extract_json():
    json_dict = {}
    extract_result = []
    with open("result.json","r",encoding='utf-8') as f:
        json_dict = json.loads(f.read())
        
        for i in json_dict['results']:
            small_result = {'name':i['name'],
                            'place_id':i['place_id'],
                            'types':i['types'][1],
                            'image':i['photos'][0]['photo_reference']}
            extract_result.append(small_result)
            #print(i['place_id'])
            #print(i['name'],end=" ")
            #print(i['types'])
            #camera(i['photos'][0]['photo_reference'])
            #cameraa(i['place_id'])
        #print(extract_result)
        with open('extract_result.json','w',encoding='utf-8') as f:
            json.dump(extract_result, f, indent=2, sort_keys=True, ensure_ascii=False) 

def camera(photo_reference,photo_name):
    '''
    url_temp = ("https://maps.googleapis.com/maps/api/place/details/json?" +
                "placeid=" + place_id +
                "&key=" + "AIzaSyCS54PJ0zmirq0QNN29mKfPaJVE0KDCiTc" +
                '')
    res = requests.get(url_temp)
    result = json.loads(res.content.decode('utf-8'))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    fo = open('detail.json', 'w')
    fo.write(json.dumps(result, ensure_ascii=False, indent=2))
    photo_reference = result['result']['photos'][0]['photo_reference']
    '''
    url_temp = ('https://maps.googleapis.com/maps/api/place/photo?' +
                'key=' + 'AIzaSyCS54PJ0zmirq0QNN29mKfPaJVE0KDCiTc' +
                '&photoreference=' + photo_reference +
                '&maxwidth=' + '600')

    res = requests.get(url_temp)

    content = BytesIO(res.content)

    print(content)
    print(type(content))
    picture = Image.open(content)
    picture.save("pictures/"+photo_name+".png",'PNG')
    '''pil_image = picture.convert('RGB')
    open_cv_image = numpy.array(pil_image)
    # Convert RGB to BGR
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    cv2.imshow('fff',open_cv_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''
    picture.show()
    """'mysql': {
    'database': 'wp2018_groupK',
    'host': 'luffy.ee.ncku.edu.tw',
    'password': 'Group_kkk_pass',
    'user': 'wp2018_groupK',
    }"""
    return content


def write_into_database():
    json_dict = {}
    with open("extract_result.json","r",encoding='utf-8') as f:
        json_dict = json.loads(f.read())
    for key in json_dict:
        print(key['name'])
        #_ref = camera(key['image'],key['name'])
        #new_site = MapSite.objects.create(name=key['name'], site_type=key['types'], location=key['place_id'],stay=key['stay'],image=f)
        new_site = MapSite(name=key['name'], site_type=key['types'], location=key['place_id'],stay=key['stay'])
        new_site.image.name = 'upload/'+key['name']+'.png'
        new_site.save()

        
#result = ["知事官邸","赤崁樓","孔廟","台南觀候所","成功大學","六千牛肉湯","莉莉冰果室","海安路"]
#result = decide_course(result)
#lists = ['藍晒圖文創園區','321巷 藝術聚落','銀同社區貓咪高地','蝸牛巷','巨大扭蛋機','神農街','壁畫','原鶯料理','警察新村彩繪村','彎曲的榕樹','文昌閣','衛民街地下道','台南雙層巴士','日本BRUTUS雜誌 國華街封面拍攝地','大成門 - 台南孔廟文化園區','新臨安橋'
#'鄭成功議和圖','明倫堂 - 台南孔廟文化園區','海安路藝術街','知事官邸苦楝樹']
#searchStay(lists)
write_into_database()
#extract_json()
#camera('CmRaAAAAsru2CaqbC-CvVK_QgmIaJ74VmkXlxq1wkjWHObfIa8aljIFRkwCsAD88gck_c7gZlNAUWzeLIBOJzHJZtWQD9ZFjn7RhlPRj9Eyo0z7deWBM1l8gT_OTkRVkT7knOM2BEhCLUe366eBnBF9ygYR7g9UOGhQQR-f4Ncj8_s1Oihvqq98qjdsffQ')