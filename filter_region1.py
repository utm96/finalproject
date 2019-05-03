# "Region": 1

from pymongo import MongoClient
mongo_uri = 'mongodb://localhost:27017'
mongo_db = 'DataTransport'
client = MongoClient(mongo_uri)
db = client[mongo_db]
collection = 'region1'
c = 'region1_detail'
# s = list(db[collection].find({}))
# print(len(s))

import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyD4n_B9MKx7XooJ6kaXkLFe-JMPhkVMsGg')

# Geocoding an address
# print(geocode_result)
# 


####### station
s = ['Hà Nội','Thành phố Hồ Chí Minh','Hải Phòng','Cần Thơ','Đà Nẵng']
for station in s:
    geocode_result = gmaps.geocode(station+ ', Việt Nam')
    db[c].insert_one({'Ten tinh,thanh pho': station,'Info':geocode_result})