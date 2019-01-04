import json
from travel.models import MapSite
def write_into_database():
    json_dict = {}
    with open("MapSiteData.json","r",encoding='utf-8') as f:
        json_dict = json.loads(f.read())
    
    
    for key in json_dict:
        print(key['name'])
        #_ref = camera(key['image'],key['name'])
        #new_site = MapSite.objects.create(name=key['name'], site_type=key['types'], location=key['place_id'],stay=key['stay'],image=f)
        site = MapSite.objects.get(name=key['name'])
        if(not site):#db裡沒有此景點
            new_site = MapSite(name=key['name'], location=key['location'],stay=key['stay'],
                        address=key['address'],phone_number=key['phone number'],site_type = key['site_type'])
            new_site.image.name = key['image']
            new_site.save()
        else:#做更新
            site.location = key['location']
            site.stay = key['stay']
            site.image.name = key['image']
            site.address=key['address']
            site.phone_number=key['phone number']
            site.site_type = key['site_type']
            site.save()

write_into_database()    