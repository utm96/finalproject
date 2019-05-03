from pymongo import MongoClient
mongo_uri = 'mongodb://localhost:27017'
mongo_db = 'DataTransport'
client = MongoClient(mongo_uri)
db = client[mongo_db]
collection = 'train_staion_detail_final'
collection_detail = 'test'
#     # import re
# # goFromRegex = "(,\s|^)"+goFrom+'(,|$)'
# # goToRegex = "(,\s|^)"+goTo+"(,|$)"
#     # goToRegex = re.compile(goToRegex, re.IGNORECASE)
#     # goFromCode = db[colection].find_one({"MaGa": "BSN"})
#     # goFromCode = db[colection].find_one({"Skeys":d})
    #   "geometry": {
    #     "location": {
    #       "lat": 21.0242529,
    #       "lng": 105.841029
    #     },
import googlemaps
import re

###################################################################################
# # distances = {k: v for k, v in sorted(distances.items(), key=lambda x: x[1])}
# # time = {k: v for k, v in sorted(time.items(), key=lambda x: x[1])}
# # AIzaSyCIFxPphkZ28jm-V6ZVlNg10F2WKtonfwE
# # gmaps = googlemaps.Client(key='AIzaSyD4n_B9MKx7XooJ6kaXkLFe-JMPhkVMsGg')
# gmaps = googlemaps.Client(key='AIzaSyCbhGuXbFO7RvpyYPCeZWlkzzTE2rBZbYc')

# # geocode_result = gmaps.geocode('67MM+QV Thái Văn, Bảo Hà, Bảo Yên, Lào Cai')
# listStation = dict()
# # db[collection_detail].update_one({'Ten ga':'Ga Thái Văn'},{'$set':  { "Info": geocode_result }})
# ListTrain = list(db[collection].find({}))

# for trainStation in ListTrain:
#     db[collection].update_one({'Ten ga':trainStation['Ten ga']},{'$set':  { "lat": trainStation['Info'][0]['geometry']["location"]["lat"], "lng": trainStation['Info'][0]['geometry']["location"]["lng"] }})
#     print(trainStation['Ten ga'])
#     # listStation[trainStation['Ten ga']] = 1
#     listStation[trainStation['Ten ga']] = [trainStation['Info'][0]['geometry']["location"]["lat"],trainStation['Info'][0]['geometry']["location"]["lng"]]

# listRegion1  = list(db['region1_detail'].find({'matrix_distance':{'$exists': False}}))
# for region in listRegion1:
#     listStation ={k: v for k, v in sorted(listStation.items(), key=lambda x: (x[1][0]-region['Info'][0]['geometry']["location"]["lat"])**2 + (x[1][1]-region['Info'][0]['geometry']["location"]["lng"])**2)}
#     listlat = list(listStation.values())
#     listKey = list(listStation.keys())[0:20]
# #     print(listStation)
# # #     print(listlat[0:20])
# #     listDistance = []
# #     print("-----------------------------")
# #     print(region["Ten tinh,thanh pho"])
# #     print(listStation)
# #     for i in range(5):
# #         m_region = gmaps.distance_matrix([[region['Info'][0]['geometry']["location"]["lat"],region['Info'][0]['geometry']["location"]["lng"]]],listlat[25*i:25*(i+1)])['rows'][0]['elements']
# #         listDistance =listDistance+ m_region
#     listDistance = gmaps.distance_matrix([[region['Info'][0]['geometry']["location"]["lat"],region['Info'][0]['geometry']["location"]["lng"]]],listlat[0:20])['rows'][0]['elements']
# #     listDistance =listDistance+ m_region

# #         # m_region = gmaps.distance_matrix([[21.0277644,105.8341598]],listlat[0:25])['rows'][0]['elements']
#     l = dict(zip(listKey,listDistance))
#     db['region1_detail'].find_one_and_update({"Ten tinh,thanh pho":region['Ten tinh,thanh pho']},{'$set':  { "matrix_distance": l }})
# # m_region = gmaps.distance_matrix([[21.0277644,105.8341598]],[[21.2187149,105.8041709],[21.0242529,105.841029]])
# # print(m_region)

# # import operator


# x = list(db['region1_detail'].find({'matrix_distance':{'$exists': True}}))
# print(len(x))
# for _ in x:
#     distances = {} 
#     time = {}
#     myDict = _['matrix_distance']

#     for key, value in myDict.items():
#         try:
#             distances[key] = value['distance']['value']
#             time[key]= value['duration']['value']
#             distances = {k: v for k, v in sorted(distances.items(), key=lambda x: x[1])}
#             time = {k: v for k, v in sorted(time.items(), key=lambda x: x[1])}

#         except:
#             continue
#     db['region1_detail'].find_one_and_update({"Ten tinh,thanh pho" : _["Ten tinh,thanh pho"]},{'$set': {'distance' : distances, "time" :time}})
    

#########################################################

def taxi_fee(dis):
    cost = 5000.0
    if(dis>25000.0):
        cost = cost + (dis - 25000.0)*12
        dis = 25000
    if(dis>10000.0):
        cost = cost + (dis - 10000.0)*14.4
        dis = 10000
    if(dis>2000):
        cost = cost + (dis - 2000)*13.1
        dis = 2000
    if(dis>0):
        cost = cost + (dis - 0)*17.4
        dis = 0
    return cost
x = list(db['region1_detail'].find({'distance':{'$exists': True}}))
print(len(x))
for _ in x:
    cost = {} 
    time = {}
    myDict = _['distance']
#     print(mtD)
    for key, value in myDict.items():
        # try:
        cost[key] = taxi_fee(float(value))
#     time[key]= value['duration']['value']
        cost = {k: v for k, v in sorted(cost.items(), key=lambda x: x[1])}
#     time = {k: v for k, v in sorted(time.items(), key=lambda x: x[1])}
        print(cost)
        # except:
        #     continue
    db['region1_detail'].find_one_and_update({"Ten tinh,thanh pho" : _["Ten tinh,thanh pho"]},{'$set': {'cost_train' : cost}})





















# goFromCode = list(db[collection_detail].find({"departure": "HAN","arrival": "DIN"}))
# print(goFromCode)
        #   "lat": 21.0277644,
        #   "lng": 105.8341598


        #   "lat": 21.2187149,
        #   "lng": 105.8041709

        #   "location": {

# m = gmaps.distance_matrix([[21.0277644,105.8341598],[21.0242529,105.841029]],[[21.2187149,105.8041709],[21.0242529,105.841029]])
# m = gmaps.directions([21.0277644,105.8341598],[21.2187149,105.8041709], mode=["transit","DRIVING"])
# print(matrix)
# db[collection_detail].insert_one({'response_matrix':m})
# print(m)
# for route in goFromCode:
#     timeString = route['timeString']
#     minute = float(re.match("(.*\s|^)(\d+) phút",timeString).group(2))
#     time = minute*60
#     s =db[collection_detail].update_one({'departure': route['departure'], 'arrival': route['arrival']},{'$set':  { "time": time }})
#     print(s)
#   "diem den": "Cần Thơ",})
# # goToCode = db[colection].find({'SKeys': { "$regex": goToRegex}})[1]['MaGa']
#     # goToCode = db[colection].find_one({$contains:{"Skeys":goTo}})['MaGa']

#     #'https://k.vnticketonline.vn/#/thongtinhanhtrinh/tau/VIN/HNO/2019-03-22'

# AIzaSyD4n_B9MKx7XooJ6kaXkLFe-JMPhkVMsGg

# https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=YOUR_API_KEY
# from pprint import pprint
# import urllib




# from datetime import datetime


# Geocoding an address
# print(geocode_result)
# 


####### station
# listStation = []
# for station in goFromCode:
#     listStation.append({'Ten ga': 'Ga '+station['TenGa'], 'MaGa':station['MaGa'] })
# print(listStation)
# for station in listStation:
#     geocode_result = gmaps.geocode(station['Ten ga'])
#     db[collection_detail].insert_one({'Ten ga': station['Ten ga'],'MaGa':station['MaGa'],'info':geocode_result })

# geocode_result = gmaps.geocode('Dọc quốc lộ 1A - Đông Hà - Quảng Trị')
# print(geocode_result)
# db[collection_detail].insert_one({'Ten ga': listStation[1]['Ten ga'],'MaGa':listStation[1]['MaGa'],'info':geocode_result })
####### station
# listAirport = []
# aiport_collection = 'airport'
# airport_detail = 'aiport_detail'
# aiports = db[aiport_collection].find({})

#   },
#   "Ten san bay": "Buôn Ma Thuột",
#   "Ma san bay": "BMV",
#   "Tinh": "Đắk Lắk",
#   "toa do": {
#     "lat": "12° 40' 1.86420'' N",
#     "lng": "108° 7' 32.97900'' E"
#   },


# for airport in aiports:
#     listAirport.append({'Ten san bay': 'Cảng hàng không '+airport['Ten san bay'], 'MaSanBay':airport['Ma san bay'] })
# print(listAirport)
# for airport in listAirport:
#     geocode_result = gmaps.geocode(airport['Ten san bay'])
#     db[airport_detail].insert_one({'Ten san bay': airport['Ten san bay'],'MaSanBay':airport['MaSanBay'],'info':geocode_result })