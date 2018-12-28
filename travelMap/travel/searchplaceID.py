import json
import requests
from PIL import Image
from io import BytesIO


# import numpy
# import cv2

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
    # return None

def detail(place_id):
    url_temp = ('https://maps.googleapis.com/maps/api/place/details/json?'+
                'key=' + "AIzaSyB2pGT9ePkt26BbSk1tvcPWXg1_8ZZ8lM8" +
                '&placeid=' + place_id +
                '&language=zh-TW'+
                '')
    print(url_temp)
    res = requests.get(url_temp)
    print(res)
    result_json = json.loads(res.content.decode('utf-8'))
    if result_json['status'] != 'OK':
        return None
    print(result_json)
    result = {}
    result['phone_number'] = result_json['result']['formatted_phone_number']
    result['address'] = result_json['result']['formatted_address']
    return result

def camera(place_id):
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

    url_temp = ('https://maps.googleapis.com/maps/api/place/photo?' +
                'key=' + 'AIzaSyCS54PJ0zmirq0QNN29mKfPaJVE0KDCiTc' +
                '&photoreference=' + photo_reference +
                '&maxwidth=' + '600')

    res = requests.get(url_temp)
    content = BytesIO(res.content)

    print(content)
    print(type(content))
    picture = Image.open(content)
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

if __name__ == '__main__':
    print(detail('ChIJcfdsmWJ2bjQRSb4_CGnFR0E'))
    # print(camera('ChIJWV77wI52bjQRGjVy2GxD-Xc'))
