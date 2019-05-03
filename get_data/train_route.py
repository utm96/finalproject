
def train(goFrom,goTo,date):
    date_train = date.strftime("%Y-%m-%d")
    url = 'https://k.vnticketonline.vn/#/thongtinhanhtrinh/tau/'+goFrom+'/'+goTo+'/'+date_train
    
    return url
import grequests
import datetime as DT 
#   "Ten ga": "Ga Hà Nội",
#   "MaGa": "HNO",
#   "Info": [
from pymongo import MongoClient

mongo_uri = 'mongodb://localhost:27017'
mongo_db = 'DataTransport'
client = MongoClient(mongo_uri)
db = client[mongo_db]
collection = 'train_staion_detail_final'
listTrainStation = list(db[collection].find({}))
today = DT.date.today()
theweekafter = today+ DT.timedelta(days=7)
for departure in listTrainStation:
    for arrival in listTrainStation:
        if(departure != arrival):
            url_train = train(departure['MaGa'],arrival['MaGa'],theweekafter)
            print(url_train)
            data_plane = {"project":"scraper","spider":"train_detail_final","url":url_train,"depart":departure['MaGa'],"dest":arrival['MaGa']}
            url = 'http://127.0.0.1:6800/schedule.json'
            req_plane = grequests.post(url,data=data_plane)
# grequests.map([req_car,req_train,req_plane])
            grequests.map([req_plane])

# url_plane = train('HNO','VIN',theweekafter)
# print(url_plane)
# data_plane = {"project":"scraper","spider":"train_detail","url":url_plane,"depart":'HNO',"dest":'VIN'}
# url = 'http://127.0.0.1:6800/schedule.json'
# req_plane = grequests.post(url,data=data_plane)
# # grequests.map([req_car,req_train,req_plane])
# grequests.map([req_plane])

# for departure in listTrainStation[:1]:
for arrival in listTrainStation:
    if('HNO' != arrival['MaGa']):
        url_train = train('HNO',arrival['MaGa'],theweekafter)
        print(url_train)
        data_plane = {"project":"scraper","spider":"train_detail","url":url_train,"depart":'HNO',"dest":arrival['MaGa']}
        url = 'http://127.0.0.1:6800/schedule.json'
        req_plane = grequests.post(url,data=data_plane)
# grequests.map([req_car,req_train,req_plane])
        grequests.map([req_plane])


