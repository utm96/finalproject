from neo4j import GraphDatabase
from pymongo import MongoClient
import re

            # data_plane = {"project":"scraper","spider":"plane_detail","url":plane_data,'code':code,"depart":fromSource,"dest":toDest}
            # url = 'http://127.0.0.1:6800/schedule.json'
            # req_car = grequests.post(url,data=data_car)

# MATCH (a:administrative_area_level_1),(b:CarStation) WHERE a.name = b.name CREATE (a)-[r:route { min_price: 0, price = 0, ave_price = 0 ,min_time: 0, time = 0, ave_time = 0 }]->(b)


mongo_uri = 'mongodb://localhost:27017'
mongo_db = 'DataTransport'
client = MongoClient(mongo_uri)
db = client[mongo_db]
# x = requests.post(url,data=j)
# print(x)
routes = list(db['train_detail_final'].find({"ListTrain": { '$exists': 'true', '$not': {'$size': 0} }}))
# routes = list(db['train_detail_final'].find({'xuat phat' : 'TCH','diem den': 'DLE'}) )
for route in routes:
    price = []
    listtime = []
    prices = []
    print(route['xuat phat'])
    for train in route['ListTrain']:
        price = price+ train['listPrice']
        timeString = train['info'].split('Thời gian hành trình:')[1].strip()
        print(timeString)
        hour = 0
        minute = 0
        day = 0
        try:
            day = float(re.match("(^|\W*)(\d+) ngày",timeString).group(2))
            print(day)
        except:
            pass
        try:
            hour = float(re.match("(.*\s|^)(\d+) giờ",timeString).group(2))
            print('------')
            print(hour)
        except:
            pass
        try:
            minute = float(re.match("(.*\s|^)(\d+) phút",timeString).group(2))
            print(minute)
        except:
            pass
        time = hour*3600 + minute*60 + day*24*3600
        if(time != 0):
            listtime.append(time)
    for i in price:
        if(i != 'Chưa có giá'):
            prices.append(float(i.replace('.','')))

    if(len(prices)>0 and len(listtime)>0):
        min_time  = min(listtime)
        ave_time = sum(listtime)/len(listtime)
        min_price = min(prices)
        max_price = max(prices)
        ave_price = sum(prices)/len(prices)
        db['route_train_detail'].find_one_and_update({'departure': route["xuat phat"], 'arrival' : route['diem den']},{'$set':{'min_price':min_price,'max_price':max_price,'ave_price':ave_price,'min_time':min_time,'ave_time':ave_time}})

# print(len( list(db['route_train_detail'].find({}))))