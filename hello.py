from pymongo import MongoClient
mongo_uri = 'mongodb://localhost:27017'
mongo_db = 'DataTransport'
client = MongoClient(mongo_uri)
db = client[mongo_db]
# collection = 'region1_detail'
collection_detail = 'test'
#     # import re
# # goFromRegex = "(,\s|^)"+goFrom+'(,|$)'
# # goToRegex = "(,\s|^)"+goTo+"(,|$)"
#     # goToRegex = re.compile(goToRegex, re.IGNORECASE)
#     # goFromCode = db[colection].find_one({"MaGa": "BSN"})
#     # goFromCode = db[colection].find_one({"Skeys":d})
import googlemaps
import re

gmaps = googlemaps.Client(key='AIzaSyD4n_B9MKx7XooJ6kaXkLFe-JMPhkVMsGg')

# geocode_result = gmaps.geocode('67MM+QV Thái Văn, Bảo Hà, Bảo Yên, Lào Cai')

# db[collection_detail].update_one({'Ten ga':'Ga Thái Văn'},{'$set':  { "Info": geocode_result }})
# goFromCode = list(db[collection_detail].find({"ListTrain": { '$exists': 'true', '$not': {'$size': 0} }}))

# goFromCode = list(db[collection_detail].find({"departure": "HAN","arrival": "DIN"}))
# print(goFromCode)
        #   "lat": 21.0277644,
        #   "lng": 105.8341598


        #   "lat": 21.2187149,
        #   "lng": 105.8041709
# matrix = gmaps.distance_matrix([[21.0277644,105.8341598]],[[21.2187149,105.8041709]])
# m = gmaps.directions([21.0277644,105.8341598],[21.2187149,105.8041709], mode=["transit","DRIVING"])
# # print(matrix)
# f= open("response.txt","w+")

# db[collection_detail].insert_one({'response':m})
# print(m)

db['aiport_detail'].update_many({},{ '$rename': { "info": "Info" } })
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