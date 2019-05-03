import math

from pymongo import MongoClient

mongo_uri = 'mongodb://localhost:27017'
mongo_db = 'DataTransport'
client = MongoClient(mongo_uri)
db = client[mongo_db]

from neo4j import GraphDatabase


print(len(list(db['car_route_detail'].find({}))))


#   "time": "80",
#   "price": "100000"

result = list(db['car_route_detail'].aggregate([{ "$group": {
        "_id": {
            "departure": "$departure",
            "arrival": "$arrival"
        },
        "price_sum" :{"$sum" : "$price"}
    }}
]))

print(len(list(db['car_route_detail_final'].find({}))))
for group in result:
    # print(group)
    list_car_route = list(db['car_route_detail'].find({ 'departure': group['_id']['departure'],'arrival': group['_id']['arrival']}))
    price_sum  = []
    time_sum = []
    for car_route in list_car_route:
        price_sum =price_sum.append(float(car_route['price']))
        time_sum =time_sum.append(float(car_route['time']))
#1 :code1, 3 : code2 , 5 :min_price , 7 :max_price,9 :ave_price, 11 :min_time , 13: time , 15 : ave_time
    ave_price = sum(price_sum)/len(list_car_route)
    ave_time = sum(time_sum)/len(list_car_route)
    min_time = min(time_sum)
    max_price = max(price_sum)
    min_price = min(price_sum)
    max_time = max(time_sum)
    db['car_route_detail_final'].insert_one({'departure': group['_id']['departure'],'arrival': group['_id']['arrival'],'ave_time' : ave_time,'ave_price':ave_price,'min_price':min_price,'max_price':max_price,'min_time':min_time,'max_time':max_time})
