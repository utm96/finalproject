
from pymongo import MongoClient

mongo_uri = 'mongodb://localhost:27017'
mongo_db = 'DataTransport'
client = MongoClient(mongo_uri)
db = client[mongo_db]


departure = 'Thành phố Vinh,nghệ an'
arrival = 'Huế, Thừa Thiên Huế'
# "Region": 1

collection = 'region1'
c = 'test'
# s = list(db[collection].find({}))
# print(len(s))

import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyD4n_B9MKx7XooJ6kaXkLFe-JMPhkVMsGg')
geocode_result = gmaps.geocode(m)
db[c].insert_one({'Info':geocode_result})