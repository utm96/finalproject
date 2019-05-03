from pymongo import MongoClient
mongo_uri = 'mongodb://localhost:27017'
mongo_db = 'DataTransport'
client = MongoClient(mongo_uri)
db = client[mongo_db]
collection = 'trainstations'
collection_detail = 'train_station_detail'
cl = 'train_staion_detail_final'
from pprint import pprint

stations = db[collection].find({})
list_station = []
for station in stations:
    list_station.append(station['ten ga'])
print(len(list_station))
lstTrain = []
# s = db[collection_detail].find_one({'Ten ga':'Ga '+ 'An Hòa'})
# print(s)
for station in list_station:
    print(station)
    s = db[collection_detail].find_one({'Ten ga':'Ga '+station})
    print(s)
    if(s != None):
        db[cl].insert_one({"Ten ga":s['Ten ga'],"MaGa": s["MaGa"],"Info": s["info"]})
        pprint(s)

pprint(len(lstTrain))

#  "Ten ga": "Ga An Hòa",
#   "MaGa": "AHO",
#   "info": [
# db[cl].insert_many(lstTrain)
