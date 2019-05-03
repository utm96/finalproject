# import urllib3
# http = urllib3.PoolManager()
# goFrom = input('diem xuat phat: ')
# goTo = input('diem den: ')
# data = {"project":"scraper","spider":"car","goFrom":goFrom}
# url = 'http://127.0.0.1:6800/schedule.json'
# req = http.request('POST',url,fields=data)
# print(req.status)

# url = 'https://vexere.com/vi-VN/ve-xe-khach-tu-'+self.goFrom+'-nghe-an-di-ha-noi-2470t1241.html?date=12-03-2019'

# 	TP. Hồ Chí Minh	Trung ương	9.297.500 (2016) [1]	 	11	Vũng Tàu	Bà Rịa - Vũng Tàu	400.777 (2013)[2]
# 2	Hà Nội	Trung ương	7.654.800 (2017) [3]	 	12	Quy Nhơn	Bình Định	457 400 (2019)[4]
# 3	Hải Phòng	Trung ương	1.980.800 (2016) [1]	 	13	Long Xuyên	An Giang	280.051 (2011)[5]
# 4	Cần Thơ	Trung ương	1.257.900 (2016) [1]	 	14	Thái Nguyên	Thái Nguyên	362.921 (2017)[6]
# 5	Biên Hòa	Đồng Nai	1.550.000 (2017) [7]	 	15	Nam Định	Nam Định	243.186 (2009)[8]
# 6	Đà Nẵng	Trung ương	1.046.200 (2016) [1]	 	16	Rạch Giá	Kiên Giang	226.316 (2009)[8]
# 7	Nha Trang	Khánh Hòa	406.000 (2015)[9]	 	17	Thủ Dầu Một	Bình Dương	244.277 (2013)[10]
# 8	Huế	Thừa Thiên - Huế	354.124 (2015)[11]	 	18	Hạ Long	Quảng Ninh	221.580 (2010)[12]
# 9	Buôn Ma Thuột	Đắk Lắk	326.135 (2009)[8]	 	19	Phan Thiết	Bình Thuận	220.560 (2012)[13]
# 10	Vinh	Nghệ An	314.351 (2014)[14]	 	20	Thanh Hóa	Thanh Hóa	393.294 (2012)[15]



def car(code,date):
    # https://vexere.com/vi-VN/ve-xe-khach-124t24701.html?date=15-03-2019
    date_car = date.strftime("%d-%m-%y")
    url  = 'https://vexere.com/vi-VN/ve-xe-khach-'+code+'.html?date='+date_car
    return url

def train(goFrom,goTo,date):
    date_train = date.strftime("%Y-%m-%d")
    # from pymongo import MongoClient
    # mongo_uri = 'mongodb://localhost:27017'
    # mongo_db = 'DataTransport'
    # client = MongoClient(mongo_uri)
    # db = client[mongo_db]
    # colection = 'station'
    # # import re
    # goFromRegex = "(,\s|^)"+goFrom+'(,|$)'
    # goToRegex = "(,\s|^)"+goTo+"(,|$)"
    # goToRegex = re.compile(goToRegex, re.IGNORECASE)
    # goFromCode = db[colection].find_one({"MaGa": "BSN"})
    # goFromCode = db[colection].find_one({"Skeys":d})

    # goFromCode = db[colection].find_one({'SKeys': { "$regex": goFromRegex}})['MaGa']
    # goToCode = db[colection].find({'SKeys': { "$regex": goToRegex}})[1]['MaGa']
    # goToCode = db[colection].find_one({$contains:{"Skeys":goTo}})['MaGa']
    # from pprint import pprint
    # pprint(goFromCode)
    #'https://k.vnticketonline.vn/#/thongtinhanhtrinh/tau/VIN/HNO/2019-03-22'
    url = 'https://k.vnticketonline.vn/#/thongtinhanhtrinh/tau/'+goFrom+'/'+goTo+'/'+date_train
    
    return url

def plane(goFrom,goTo,date):
    # 'https://www.google.com/flights?lite=0#flt=HAN.SGN.2019-03-19;c:VND;e:1;sd:1;t:f;tt:o'
    # https://www.google.com/flights?lite=0#flt=HAN.SGN.2019-03-19;c:VND;e:1;s:1;sd:1;t:f;tt:o
    date_plane = date.strftime("%Y-%m-%d")
    url = 'https://www.google.com/flights?lite=0#flt='+goFrom+'.'+goTo+'.'+date_plane+';c:VND;e:1;s:1;sd:1;t:f;tt:o'
    return url
import grequests
import datetime as DT 
# 124t24701
from pymongo import MongoClient
CITY = ["Vinh - Nghệ An","Hà Nội","Hải Phòng","Cần Thơ","Vũng Tàu - Bà Rịa-Vũng Tàu","Hồ Chí Minh","Đà Nẵng","Huế - Thừa Thiên-Huế"]

mongo_uri = 'mongodb://localhost:27017'
mongo_db = 'DataTransport'
client = MongoClient(mongo_uri)
db = client[mongo_db]
colection = 'car_station'
today = DT.date.today()
tomorow = today+ DT.timedelta(days=1)
for fromSource in CITY:
    location = db[colection].find_one({"value": fromSource})
    fromStateId = location['StateId']
    fromCityId = location['CityId']
    codeFrom = ''
    if(fromCityId == 0):
        codeFrom = '1'+ str(fromStateId)
    else:
        codeFrom = '2'+ str(fromCityId) 

    try:
        train_depart = db["station"].find_one({"StateId": fromStateId, "CityId":fromCityId})['MaGa']
    except:
        train_depart = ''

    try:
        plane_depart = db["airport"].find_one({"StateId": fromStateId, "CityId":fromCityId})['Ma san bay']
    except:
        plane_depart = ''
    for toDest in CITY:
        if(toDest != fromSource):
            dest = db[colection].find_one({"value": toDest})
            toStateId = dest['StateId']
            toCityId = dest['CityId']
            codeTo = ''
            if(toCityId == 0):
                codeTo = '1'+ str(toStateId)  + '1'
            else:
                codeTo = '2'+str(toCityId) + '1'
            code = codeFrom + 't' + codeTo
            train_data = ''
            if(train_depart != ''):
                try:
                    train_dest = db["station"].find_one({"StateId": toStateId, "CityId":toCityId})['MaGa']
                except:
                    train_dest = ''
                if(train_dest != ''):
                    train_data = train(train_depart,train_dest,tomorow)
            plane_data = ''
            if(plane_depart != ''):
                try:
                    plane_dest = db["airport"].find_one({"StateId": toStateId, "CityId":toCityId})['Ma san bay']
                except:
                    plane_dest = ''
                if(plane_dest != ''):
                    plane_data = plane(plane_depart,plane_dest,tomorow)
            car_data = car(code,tomorow)
        # print(plane_data)
        # print(car_data)
            print(train_data)
            print("------------------------")
            data_car = {"project":"scraper","spider":"car_detail","url":car_data,'code':code,"depart":fromSource,"dest":toDest}
            data_train = {"project":"scraper","spider":"train_detail","url":train_data,'code':code,"depart":fromSource,"dest":toDest}
            data_plane = {"project":"scraper","spider":"plane_detail","url":plane_data,'code':code,"depart":fromSource,"dest":toDest}
            url = 'http://127.0.0.1:6800/schedule.json'
            req_car = grequests.post(url,data=data_car)
            req_train = grequests.post(url,data=data_train)
            req_plane = grequests.post(url,data=data_plane)
            # grequests.map([req_car,req_train,req_plane])
            grequests.map([req_train])


