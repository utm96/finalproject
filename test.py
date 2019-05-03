import math

from pymongo import MongoClient

mongo_uri = 'mongodb://localhost:27017'
mongo_db = 'DataTransport'
client = MongoClient(mongo_uri)
db = client[mongo_db]

from neo4j import GraphDatabase

import googlemaps
import re

# gmaps = googlemaps.Client(key='AIzaSyD4n_B9MKx7XooJ6kaXkLFe-JMPhkVMsGg')
gmaps = googlemaps.Client(key='AIzaSyCbhGuXbFO7RvpyYPCeZWlkzzTE2rBZbYc')



uri = "bolt://localhost"
driver = GraphDatabase.driver(uri, auth=("neo4j", "123a!@#A"))

m = 'đống đa,hà nội'

#tinh khoang cach
# def distance_on_unit_sphere(lat1, long1, lat2, long2):


#     degrees_to_radians = math.pi/180.0

#     phi1 = (90.0 - lat1)*degrees_to_radians
#     phi2 = (90.0 - lat2)*degrees_to_radians

#     # theta = longitude
#     theta1 = long1*degrees_to_radians
#     theta2 = long2*degrees_to_radians
#     cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
#     math.cos(phi1)*math.cos(phi2))

#     return arc


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

def get_level(address_components):
    result = {}
    i = 0
    for component in address_components:
        if 'administrative_area_level_1'  in component['types']:
            i += 1
            print(component['long_name'])
            result['administrative_area_level_1'] = component['long_name']
        if ('locality' in component['types']) or ('administrative_area_level_2' in component['types']) or ('route' in component['types']) or ('sublocality_level_1'  in component['types']):
            i +=1
            result['level_'+str(i)] = component['long_name']
    return result

def b(text):
    for ch in ['\\','`','*','_','{','}','[',']','(',')','>','#','+','-','.','!','$','\''," ",',']:
        text = text.replace(ch,"")
    return text
def create_level(graphDB_Session,name,long_name,short_name,lat,lng,level,nameParent,levelParent):
    query_create  = ['CREATE (',"",":"+level+" { name:'","","',lat : ","",", lng:","",", long_name:'","","', short_name:'","","'})"]
    query_car  = ['CREATE (',"",":CarStation { name:'","","', long_name:'","","', short_name:'","","'})"]
    query_train  = ['CREATE (',"",":TrainStation { name:'","","', long_name:'","","', short_name:'","","'})"]
    query_plane  = ['CREATE (',"",":PlaneStation { name:'","","', long_name:'","","', short_name:'","","'})"]
    # query_car  = ['CREATE (',"",":BoardStation { name:'","","'})"]

    query_car_relation ="MATCH (a:"+level+"),(b:CarStation) WHERE a.name = b.name CREATE (a)-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]->(b)"
    query_train_relation ="MATCH (a:"+level+"),(b:TrainStation) WHERE a.name = b.name CREATE (a)-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]->(b)"
    query_plane_relation ="MATCH (a:"+level+"),(b:PlaneStation) WHERE a.name = b.name CREATE (a)-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]->(b)"
    query_car1_relation ="MATCH (a:"+level+"),(b:CarStation) WHERE a.name = b.name CREATE (a)<-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]-(b)"
    query_train1_relation ="MATCH (a:"+level+"),(b:TrainStation) WHERE a.name = b.name CREATE (a)<-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]-(b)"
    query_plane1_relation ="MATCH (a:"+level+"),(b:PlaneStation) WHERE a.name = b.name CREATE (a)<-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]-(b)"
    query_parent_relation ="MATCH (a:"+levelParent+"),(b:"+level+") WHERE a.name ='"+nameParent+"' and b.long_name = '"+long_name+"' CREATE (a)-[r:child]->(b)"

    #1 :node, 3 : tên , 5 :lat , 7 :lng , 9 : long_name, 11: short_name
    query_create[1] = b(name)
    query_create[3] = name
    query_create[5] = lat 
    query_create[7] = lng
    query_create[9] = long_name
    query_create[11] = short_name

    query_car[1] = b(name)+'_car'
    query_car[3] = name
    query_car[5] = long_name
    query_car[7] = short_name

    query_train[1] = b(name)+'_train'
    query_train[3] = name       
    query_train[5] = long_name
    query_train[7] = short_name


    query_plane[1] = b(name)+'_plane'
    query_plane[3] = name
    query_plane[5] = long_name
    query_plane[7] = short_name

    print(''.join(query_car))
    print(''.join(query_create))

    print(''.join(query_plane))

    graphDB_Session.run(''.join(query_create))

    graphDB_Session.run(''.join(query_plane))
    graphDB_Session.run(''.join(query_train))
    graphDB_Session.run(''.join(query_car))
    print(query_car_relation)
    graphDB_Session.run(query_car_relation)
    graphDB_Session.run(query_car1_relation)
    graphDB_Session.run(query_train_relation)
    graphDB_Session.run(query_train1_relation)
    graphDB_Session.run(query_plane_relation)
    graphDB_Session.run(query_plane1_relation)
    print(query_parent_relation)
    graphDB_Session.run(query_parent_relation)


def maxtrix_distance(lat,lng,mode):
    #mode = 0 : car ; mode = 1 : 'plane' ; mode = 2 : train
    # car : 20 , plan :3 , train : 20
    db_collection = 'car_station_detail'
    i = 20
    name = 'dia chi'
    if(mode == 0):
        db_collection = 'car_station_detail'
        i = 20
        name = 'dia chi'
    if(mode == 1):
        db_collection = 'aiport_detail' 
        i  = 3
        name = 'MaSanBay'
    if(mode == 2):
        db_collection = 'train_staion_detail_final'
        i = 20
        name = 'Ten ga'
    listA = dict()
    listStation = list(db[db_collection].find({}))
    print(len(listStation))
    for station in listStation:
        db[db_collection].update_one({name:station[name]},{'$set':  { "lat": station['Info'][0]['geometry']["location"]["lat"], "lng": station['Info'][0]['geometry']["location"]["lng"] }})
        listA[station[name]] = [station['Info'][0]['geometry']["location"]["lat"],station['Info'][0]['geometry']["location"]["lng"]]

    listA ={k: v for k, v in sorted(listA.items(), key=lambda x:  (x[1][0]-lat)**2 + (x[1][1]-lng)**2)}
    listlat = list(listA.values())
    listKey = list(listA.keys())[0:i]

    listDistance = gmaps.distance_matrix([[lat,lng]],listlat[0:i])['rows'][0]['elements']
    l = dict(zip(listKey,listDistance))
    distances = {} 
    time = {}
    for key, value in l.items():
        try:
            distances[key] = value['distance']['value']
            time[key]= value['duration']['value']
            distances = {k: v for k, v in sorted(distances.items(), key=lambda x: x[1])}
            time = {k: v for k, v in sorted(time.items(), key=lambda x: x[1])}

        except:
            continue
    return {'distance' : distances, "time" :time}


# collection = 'region1'
# c = 'test'
# s = list(db[collection].find({}))
# print(len(s))



# s = ['Hà Nội','Thành phố Hồ Chí Minh','Hải Phòng','Cần Thơ','Đà Nẵng']
# for station in s:

def create_train_distance(graphDB_Session,long_name,listTrain_cost,listTrain_time):
    print(listTrain_cost)
    print(listTrain_time)
    for k,v in listTrain_cost.items():
        query_train_route = ["MATCH (a:TrainStation {name:'","","'}),(b:TrainStop {name:\"","","\"}) CREATE (a)-[r:route { min_price:","",", max_price :","",", ave_price :" ,"", ",min_time:","",", time : ","",", ave_time : ","",", type : 'driving'}]->(b)"]
        query_train_route1 = ["MATCH (a:TrainStation {name:'","","'}),(b:TrainStop {name:\"","","\"}) CREATE (a)<-[r:route { min_price:","",", max_price :","",", ave_price :" ,"", ",min_time:","",", time : ","",", ave_time : ","",", type : 'driving'}]-(b)"]

        query_train_route[1] = long_name
        query_train_route[3] = k
        query_train_route[5] = str(v)
        query_train_route[7] = str(v)
        query_train_route[9] = str(v)
        query_train_route[11] = str(listTrain_time[k])
        query_train_route[13] = str(listTrain_time[k])
        query_train_route[15] = str(listTrain_time[k])

        query_train_route1[1] = long_name
        query_train_route1[3] = k
        query_train_route1[5] = str(v)
        query_train_route1[7] = str(v)
        query_train_route1[9] = str(v)
        query_train_route1[11] = str(listTrain_time[k])
        query_train_route1[13] = str(listTrain_time[k])
        query_train_route1[15] = str(listTrain_time[k])
        graphDB_Session.run(''.join(query_train_route))
        graphDB_Session.run(''.join(query_train_route1))

def create_car_distance(graphDB_Session,long_name,listCar_cost,listCar_time):
    for k,v in listCar_cost.items():
        query_car_route = ["MATCH (a:CarStation {name:'","","'}),(b:CarStop {address:\"","","\"}) CREATE (a)-[r:route { min_price:","",", max_price :","",", ave_price :" ,"", ",min_time:","",", time : ","",", ave_time : ","",", type : 'driving'}]->(b)"]
        query_car_route1 = ["MATCH (a:CarStation {name:'","","'}),(b:CarStop {address:\"","","\"}) CREATE (a)<-[r:route { min_price:","",", max_price :","",", ave_price :" ,"", ",min_time:","",", time : ","",", ave_time : ","",", type : 'driving'}]-(b)"]

        query_car_route[1] = long_name
        query_car_route[3] = k
        query_car_route[5] = str(v)
        query_car_route[7] = str(v)
        query_car_route[9] = str(v)
        query_car_route[11] = str(listCar_time[k])
        query_car_route[13] = str(listCar_time[k])
        query_car_route[15] = str(listCar_time[k])

        query_car_route1[1] = long_name
        query_car_route1[3] = k
        query_car_route1[5] = str(v)
        query_car_route1[7] = str(v)
        query_car_route1[9] = str(v)
        query_car_route1[11] = str(listCar_time[k])
        query_car_route1[13] = str(listCar_time[k])
        query_car_route1[15] = str(listCar_time[k])
        graphDB_Session.run(''.join(query_car_route))
        graphDB_Session.run(''.join(query_car_route1))


def create_plane_distance(graphDB_Session,long_name,listPlane_cost,listPlane_time):
    for k,v in listPlane_cost.items():
        query_plane_route = ["MATCH (a:PlaneStation {name:'","","'}),(b:Airport {code:\"","","\"}) CREATE (a)-[r:route { min_price:","",", max_price :","",", ave_price :" ,"", ",min_time:","",", time : ","",", ave_time : ","",", type : 'driving'}]->(b)"]
        query_plane_route1 = ["MATCH (a:PlaneStation {name:'","","'}),(b:CarStop {code:\"","","\"}) CREATE (a)<-[r:route { min_price:","",", max_price :","",", ave_price :" ,"", ",min_time:","",", time : ","",", ave_time : ","",", type : 'driving'}]-(b)"]

        query_plane_route[1] = long_name
        query_plane_route[3] = k
        query_plane_route[5] = str(v)
        query_plane_route[7] = str(v)
        query_plane_route[9] = str(v)
        query_plane_route[11] = str(listPlane_time[k])
        query_plane_route[13] = str(listPlane_time[k])
        query_plane_route[15] = str(listPlane_time[k])

        query_plane_route1[1] = long_name
        query_plane_route1[3] = k
        query_plane_route1[5] = str(v)
        query_plane_route1[7] = str(v)
        query_plane_route1[9] = str(v)
        query_plane_route1[11] = str(listPlane_time[k])
        query_plane_route1[13] = str(listPlane_time[k])
        query_plane_route1[15] = str(listPlane_time[k])
        graphDB_Session.run(''.join(query_plane_route))
        graphDB_Session.run(''.join(query_plane_route1))



geocode_result = gmaps.geocode(m)
db['test'].insert_one({'info':geocode_result})
x = (get_level(reversed(geocode_result[0]['address_components'])))
# print(x)
# # match (lv1:administrative_area_level_1) -[:parent]-(lv2:lv2 {long_name :'HaNoi'}) return lv2
# with driver.session() as graphDB_Session:
#     listGeoCodeString = []
#     y = {}
#     y['administrative_area_level_1'] = x['administrative_area_level_1']
#     geocode_string =  x['administrative_area_level_1']
#     listGeoCodeString.append(geocode_string)
#     query = "match (lv1:administrative_area_level_1 {name :'"+ x['administrative_area_level_1']+"'})"
#     for i in range(2,len(x)+1):
#         geocode_string = x['level_'+str(i)] +', '+ geocode_string
#         listGeoCodeString.append(geocode_string)
#         y['level_'+str(i)] = x['level_'+str(i)]
#         query +=  "-[:child]->(lv"+str(i)+" :level_"+str(i)+" {name:'"+geocode_string+"'})"
#         print(query + "return lv"+str(i))
#         results = graphDB_Session.run(query + "return lv"+str(i))
#         records = []
#         for record in results:
#             records.append(record)
#         print("------------------"+str(len(records)))
#         if(len(records) == 0):
#             print(geocode_string)
#             info = gmaps.geocode(geocode_string)[0]
#             long_name = info['address_components'][0]['long_name']
#             short_name = info['address_components'][0]['short_name']
#             lat = info['geometry']['location']['lat']
#             lng = info['geometry']['location']['lng']
#             car_distance = maxtrix_distance(lat,lng,0)
#             cost_car = {} 
#             for key, value in car_distance['distance'].items():
#                 cost_car[key] = taxi_fee(float(value))
#                 cost_car = {k: v for k, v in sorted(cost_car.items(), key=lambda x: x[1])}

#             train_distance = maxtrix_distance(lat,lng,2)
#             cost_train = {} 
#             for key, value in train_distance['distance'].items():
#                 cost_train[key] = taxi_fee(float(value))
#                 cost_train = {k: v for k, v in sorted(cost_train.items(), key=lambda x: x[1])}

#             plane_distance = maxtrix_distance(lat,lng,1)
#             cost_plane = {} 
#             for key, value in plane_distance['distance'].items():
#                 cost_plane[key] = taxi_fee(float(value))
#                 cost_plane = {k: v for k, v in sorted(cost_plane.items(), key=lambda x: x[1])}
#             db['level_'+str(i)].insert_one({'name': geocode_string, 'info' : info, 'long_name': geocode_string, ' short_name' : short_name, 'lat' : lat, 'lng':lng,'parent': y
#                 ,'cost_car' : cost_car, 'time_car': car_distance['time'],'distance_car' : car_distance['distance'],
#                 'cost_train' : cost_train, 'time_train': train_distance['time'],'distance_train' : train_distance['distance'],
#                 'cost_plane' : cost_plane, 'time_plane': plane_distance['time'],'distance_plane' : plane_distance['distance']})


#             if(i == 2):
#                 levelParent = 'administrative_area_level_1'
#             else : 
#                 levelParent = 'level_'+str(i-1)
#             create_level(graphDB_Session,geocode_string,geocode_string,short_name,str(lat),str(lng),"level_"+str(i),listGeoCodeString[-2],levelParent)
#             create_train_distance(graphDB_Session,geocode_string,cost_train,train_distance['time'])
#             create_car_distance(graphDB_Session,geocode_string,cost_car,car_distance['time'])
#             create_plane_distance(graphDB_Session,geocode_string,cost_plane,plane_distance['time'])



