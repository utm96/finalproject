# "Region": 1

from pymongo import MongoClient
mongo_uri = 'mongodb://localhost:27017'
mongo_db = 'DataTransport'
client = MongoClient(mongo_uri)
db = client[mongo_db]
collection = 'car_route'
c = 'car_station_detail'
s = list(db[collection].find({}))
print(len(s))

import googlemaps
from datetime import datetime

# gmaps = googlemaps.Client(key='AIzaSyD4n_B9MKx7XooJ6kaXkLFe-JMPhkVMsGg')
# gmaps = googlemaps.Client(key='AIzaSyD4n_B9MKx7XooJ6kaXkLFe-JMPhkVMsGg')
gmaps = googlemaps.Client(key='AIzaSyCbhGuXbFO7RvpyYPCeZWlkzzTE2rBZbYc')
# Geocoding an address
# print(geocode_result)
# 
#   "tinh,thanh pho": "Hà Nội",
#   "dia chi": "25 T1 Hoàng Đạo Thúy - Thanh Xuân - Hà Nội"
# }

####### station
# s = ['Hà Nội','Thành phố Hồ Chí Minh','Hải Phòng','Cần Thơ','Đà Nẵng']
for station in s:
    # print(station['dia chi'])
    l = list(db[c].find({'dia chi': station['dia chi']}))
    if(len(l) == 0):
        geocode_result = gmaps.geocode(station['dia chi'])
        db[c].insert_one({'tinh,thanh pho': station['tinh,thanh pho'],'dia chi': station['dia chi'],'Info':geocode_result})