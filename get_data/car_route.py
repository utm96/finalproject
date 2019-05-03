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

import grequests
import datetime as DT 
# 124t24701
from pymongo import MongoClient
# CITY = ["Vinh - Nghệ An","Hà Nội","Hải Phòng","Cần Thơ","Vũng Tàu - Bà Rịa-Vũng Tàu","Hồ Chí Minh","Đà Nẵng","Huế - Thừa Thiên-Huế"]

mongo_uri = 'mongodb://localhost:27017'
mongo_db = 'DataTransport'
client = MongoClient(mongo_uri)
db = client[mongo_db]
colection = 'car_station'
today = DT.date.today()
tomorow = today+ DT.timedelta(days=7)
# db[colection].find_one_and_delete({"CityId": 0,'Category': 'Language.StateCity','value':'Sài Gòn'})
# db[colection].find_one_and_delete({"CityId": 0,'Category': 'Language.StateCity','value':'Kẻ Bàng - Quảng Bình'})
# db[colection].find_one_and_delete({"CityId": 0,'Category': 'Language.StateCity','value':'Sơn Đoòng - Quảng Bình'})
locations = list(db[colection].find({"CityId": 0,'Category': 'Language.StateCity'}))
# print(len(locations))
for departure in locations:
    codeFrom = '1'+ str(departure['StateId'])
    for arrival in locations:
        if(arrival != departure) :
            codeTo = '1'+ str(arrival['StateId'])  + '1'
            code = codeFrom + 't' + codeTo
            car_data = car(code,tomorow)
            # print(plane_data)
            # print(car_data)
            print(car_data)
            print("------------------------")
            data_car = {"project":"scraper","spider":"car_route_detail","url":car_data}
            # data_train = {"project":"scraper","spider":"train_detail","url":train_data,'code':code,"depart":fromSource,"dest":toDest}
            # data_plane = {"project":"scraper","spider":"plane_detail","url":plane_data,'code':code,"depart":fromSource,"dest":toDest}
            url = 'http://127.0.0.1:6800/schedule.json'
            req_car = grequests.post(url,data=data_car)
            # req_train = grequests.post(url,data=data_train)
            # req_plane = grequests.post(url,data=data_plane)
            # grequests.map([req_car,req_train,req_plane])
            grequests.map([req_car])
# for l in locations:
# print(locations)
