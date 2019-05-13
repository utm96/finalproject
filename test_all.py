import math

from pymongo import MongoClient

mongo_uri = 'mongodb://localhost:27017'
mongo_db = 'DataTransport'
client = MongoClient(mongo_uri)
db = client[mongo_db]
import googlemaps

from neo4j import GraphDatabase

# d1  = {'a':1,'b':2}
# d2 = {'a':3,'c':4}
# print(d1)
# d1.update(d2)
# print(d1)
# # print(len(list(db['car_route_detail'].find({}))))
# listRegion1  = list(db['region1_detail'].find())
# print(len(listRegion1))
# for region in listRegion1:
#     l1 = db['region1_detail'].find_one_and_update({"Ten tinh,thanh pho":region['Ten tinh,thanh pho']},{'$set':{'place_id' : region['Info'][0]['place_id']}})
# #     if(len(l1)!=60):
#     print(len(l1))
# #   "time": "80",
#   "price": "100000"

#   "xuat phat": "HNO",
#   "diem den": "QNH",
#   "ListTrain": []
# print(list(db['route_train_detail'].find({'departure' : 'VIN','arrival': 'SGO'}) ))
#   "departure": " - Vĩnh Long - Vĩnh Long",
#   "arrival": "Cầu Kè",


# CarStop {name : '05 Nguyễn Thái Học - Vinh - Nghệ An'})<-[r:route]-(a:CarStop {name : '01 Ngọc Hồi, Hoàng Liệt - Hoàng Mai - Hà Nội'}
# print(list(db['car_station_detail'].find({"dia chi": "Dọc Quốc Lộ 1A - Hà Tĩnh - Hà Tĩnh"}) ))

# import re
# hour = float(re.match("(.*\s|^)(\d+) giờ",'1 ngày 1 giờ 44 phút').group(2))
# print(hour)
# l = []
# l.append("d")
# l.append("c")
# l.append("dsa")
# print(l)
# for i in range(len(l)):
#     l.remove(l[i])

gmaps = googlemaps.Client(key='AIzaSyCbhGuXbFO7RvpyYPCeZWlkzzTE2rBZbYc')
# {'long_name': 'Nam Dinh', 'short_name': 'Nam Dinh', 'types': ['administrative_area_level_1', 'political']}
component = {'long_name': 'Ho Chi Minh', 'short_name': 'Ho Chi Minh', 'types': ['administrative_area_level_1', 'political']}
ad1 = gmaps.geocode('Ninh Bình',components =  {'long_name': 'Ninh Bình', 'short_name': 'Ninh Bình', 'types': ['administrative_area_level_1', 'political'],'country':'VN'})
print(ad1)

import re


# def no_accent_vietnamese(s):
#     s.encode('utf-8').decode('utf-8')
#     s = re.sub(u'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
#     s = re.sub(u'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
#     s = re.sub(u'èéẹẻẽêềếệểễ', 'e', s)
#     s = re.sub(u'ÈÉẸẺẼÊỀẾỆỂỄ', 'E', s)
#     s = re.sub(u'òóọỏõôồốộổỗơờớợởỡ', 'o', s)
#     s = re.sub(u'ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ', 'O', s)
#     s = re.sub(u'ìíịỉĩ', 'i', s)
#     s = re.sub(u'ÌÍỊỈĨ', 'I', s)
#     s = re.sub(u'ùúụủũưừứựửữ', 'u', s)
#     s = re.sub(u'ƯỪỨỰỬỮÙÚỤỦŨ', 'U', s)
#     s = re.sub(u'ỳýỵỷỹ', 'y', s)
#     s = re.sub(u'ỲÝỴỶỸ', 'Y', s)
#     s = re.sub(u'Đ', 'D', s)
#     s = re.sub(u'đ', 'd', s)
#     return s.encode('utf-8')

# print(no_accent_vietnamese('hồ chí minh'))
def no_accent_vietnamese(s):
    s = s.encode('utf-8').decode('utf-8')
    s = re.sub(u'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(u'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(u'èéẹẻẽêềếệểễ', 'e', s)
    s = re.sub(u'ÈÉẸẺẼÊỀẾỆỂỄ', 'E', s)
    s = re.sub(u'òóọỏõôồốộổỗơờớợởỡ', 'o', s)
    s = re.sub(u'ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ', 'O', s)
    s = re.sub(u'ìíịỉĩ', 'i', s)
    s = re.sub(u'ÌÍỊỈĨ', 'I', s)
    s = re.sub(u'ùúụủũưừứựửữ', 'u', s)
    s = re.sub(u'ƯỪỨỰỬỮÙÚỤỦŨ', 'U', s)
    s = re.sub(u'ỳýỵỷỹ', 'y', s)
    s = re.sub(u'ỲÝỴỶỸ', 'Y', s)
    s = re.sub(u'Đ', 'D', s)
    s = re.sub(u'đ', 'd', s)
    return s.encode('utf-8')



def convert(text):
    patterns = {
    '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
    '[đ]': 'd',
    '[èéẻẽẹêềếểễệ]': 'e',
    '[ìíỉĩị]': 'i',
    '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
    '[ùúủũụưừứửữự]': 'u',
    '[ỳýỷỹỵ]': 'y',
    'Đ': 'D',
    '[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]': 'A',
    '[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]': 'O',
    '[ÌÍỊỈĨ]': 'I',
    '[ƯỪỨỰỬỮÙÚỤỦŨ]': 'U',
    '[ÌÍỊỈĨ]': 'I',
    '[ÈÉẸẺẼÊỀẾỆỂỄ]': 'E'
    }
    output = text
    for regex, replace in patterns.items():
        output = re.sub(regex, replace, output)
        # deal with upper case
        # output = re.sub(regex.upper(), replace.upper(), output)
    return output

if __name__ == '__main__':
    print(convert("Hồ Chí Minh"))
    # print no_accent_vietnamese("Welcome to Vietnam !")
    # print no_accent_vietnamese("VIỆT NAM ĐẤT NƯỚC CON NGƯỜI")