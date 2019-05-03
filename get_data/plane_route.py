
def plane(goFrom,goTo,date):
    # 'https://www.google.com/flights?lite=0#flt=HAN.SGN.2019-03-19;c:VND;e:1;sd:1;t:f;tt:o'
    # https://www.google.com/flights?lite=0#flt=HAN.SGN.2019-03-19;c:VND;e:1;s:1;sd:1;t:f;tt:o
    # https://www.google.com/flights?lite=0#flt=HAN.SGN.2019-04-08;c:VND;e:1;s:0;sd:1;t:f;tt:o
    date_plane = date.strftime("%Y-%m-%d")
    url = 'https://www.google.com/flights?lite=0#flt='+goFrom+'.'+goTo+'.'+date_plane+';c:VND;e:1;s:0;sd:1;t:f;tt:o'
    return url
import grequests
import datetime as DT 
# 124t24701
# MaSanBay
from pymongo import MongoClient

mongo_uri = 'mongodb://localhost:27017'
mongo_db = 'DataTransport'
client = MongoClient(mongo_uri)
db = client[mongo_db]
collection = 'aiport_detail'
listAirport = list(db[collection].find({}))
today = DT.date.today()
theweekafter = today+ DT.timedelta(days=7)
# for departure in listAirport:
#     for arrival in listAirport:
#         if(departure != arrival):
#             url_plane = plane(departure['MaSanBay'],arrival['MaSanBay'],theweekafter)
#             print(url_plane)
#             data_plane = {"project":"scraper","spider":"plane_detail","url":url_plane,"depart":departure['MaSanBay'],"dest":arrival['MaSanBay']}
#             url = 'http://127.0.0.1:6800/schedule.json'
#             req_plane = grequests.post(url,data=data_plane)
# # grequests.map([req_car,req_train,req_plane])
#             grequests.map([req_plane])

url_plane = plane('HAN','DIN',theweekafter)
print(url_plane)
data_plane = {"project":"scraper","spider":"plane_detail","url":url_plane,"depart":'HAN',"dest":'DIN'}
url = 'http://127.0.0.1:6800/schedule.json'
req_plane = grequests.post(url,data=data_plane)
# grequests.map([req_car,req_train,req_plane])
grequests.map([req_plane])


