from test import Node,UsePlan,DayRoute,Option

from controller import controllerFindRoute

#listNodeUnschedule

import math
# from test import find_route
from pymongo import MongoClient
from neo4j import GraphDatabase
import googlemaps
import re
# from test import 

def upateF(listNodeUnschedule,listRoute,listOption,gmaps,driver,db):
    for node in listNodeUnschedule:
        for m in range(len(listRoute)):
            route = listRoute[m]
            print("route : "+str(m))
            for i in range(1,len(route)):
                print("position " + str(i))
                resultCheckInsert = canInsert(node,route,i,gmaps,driver,db)
                if (resultCheckInsert['check']):
                    o = Option(m,i,node,ration(route,node,i,gmaps,driver,db),0,resultCheckInsert['route'])
                    listOption.append(o)
                    print("len option : " +str(len(listOption)))
    
    listOption = sorted(listOption, key=lambda x: x.sumRation, reverse=True)
    print("list option : ---------------------------")
    for o in listOption:
        print(o)
    listOption = listOption[:(len(listOption)+2)//2]
    #sorte listOption by the ration descending
    #get the f first best option
    #get rid of duplicate

    print("list option  selected: ---------------------------")
    for o in listOption:
        print(o)
    return listOption


def setStartEnd(nodePrev,node,gmaps,driver,db):
    t_start = nodePrev.endTime + getFee(nodePrev,node,gmaps,driver,db)
    if(t_start > node.earliestTime):
        node.startTime = t_start
        node.endTime = node.startTime + node.serviceTime
    else:
        node.startTime = node.earliestTime
        node.endTime = node.startTime + node.serviceTime

def canInsert(node,route,i,gmaps,driver,db):
    print(route)
    print(node)
    nodePrev = route[i-1]
    nodePost = route[i]

    #condition1 : startTime, endTime in the interval e,l
    #statTime : nodePrve.endTime + getFee(nodePrev,node) > node.earliestTime : nodePrve.endTime + getFee(nodePrev,node) ? node.ealiestTime
    t_start = nodePrev.endTime + getFee(nodePrev,node,gmaps,driver,db)
    if(t_start > node.earliestTime):
        node.startTime = t_start
        node.endTime = node.startTime + node.serviceTime
    else:
        node.startTime = node.earliestTime
        node.endTime = node.startTime + node.serviceTime
    subCon1 = node.startTime >= node.earliestTime
    subCon2 = node.endTime  <= node.lastestTime
    print("startCondition : " + str(subCon1) + " , endCondition : " + str(subCon2))
    check  = node.startTime >= node.earliestTime and node.endTime <= node.lastestTime


    #check the rest of post node
    # deltaTime = 
    from copy import deepcopy
    routeCheck = route[i:len(route)]
    routeCheck = deepcopy(routeCheck)
    _ = deepcopy(node)
    routeCheck.insert(0,_)
    if check == True:
        for k in range (1, len(routeCheck)):
            setStartEnd(routeCheck[k-1],routeCheck[k],gmaps,driver,db)
            if (not(routeCheck[k].startTime >= routeCheck[k].earliestTime and routeCheck[k].endTime <= routeCheck[k].lastestTime)):
                check = False
                break
    # listCheck.append(condition1)
    
        # nodeToCheck = nodeCurr
            #condition2 
    # node.endTime + getFee(node,nodePost) 



    # condition1 = nodePost.earliestTime - node.serviceTime - getFee(node,nodePost,gmaps,driver,db)> node.earliestTime
    # print("con1 :==========="+str(condition1) + "===========================")
    # condition2 = node.earliestTime > nodePrev.earliestTime + nodePrev.serviceTime + getFee(nodePrev,node,gmaps,driver,db)
    # print("con2 :==========="+str(condition2) + "===========================")
    # print("node.earliestTime : "+ str(node.earliestTime))
    # print("nodePrev.earliestTime :"+ str(nodePrev.earliestTime))
    # print("getFee(nodePrev,node,gmaps,driver,db): "+str(getFee(nodePrev,node,gmaps,driver,db)))
    # print("nodePrev.serviceTime : "+ str(nodePrev.serviceTime))
    # #condition1 : nodePost['timeStart'] - node['serviceTime'] - fee(node-nodePost)> node['earliestTime'] > nodePrev['timeStart] + nodePre['timeService'] + fee[nodePre - node]
    # if (nodePost.earliestTime - node.serviceTime - getFee(node,nodePost,gmaps,driver,db)> node.earliestTime and   node.earliestTime > nodePrev.earliestTime + nodePrev.serviceTime + getFee(nodePrev,node,gmaps,driver,db)):
    #     # listOption add {node ,route,i}
    #     print("can insert")
    #     return True
    # else:
    #     print("cant insert")

    #     return False
    return {'check': check, 'route' : routeCheck}

def getFee(nodeDeparture,nodeArrival,gmaps,driver,db):

    if (nodeArrival.address in nodeDeparture.fee):
        return nodeDeparture.fee[nodeArrival.address]
    # x = controllerFindRoute()
    a = nodeArrival.address
    d = nodeDeparture.address
    cost = find_route(d,a,gmaps,driver,db)
    if (cost != None):
        nodeDeparture.fee[nodeArrival.address] = cost
        return cost
    else :    
        return 999999


def selectOption(lstOption):
    import random
    sumRation = 0
    for option in lstOption:
        sumRation = sumRation + option.sumRation
    for option in lstOption:
        option.prob = option.sumRation/sumRation  

    u = random.random()
    accumProb = 0
    for option in lstOption:
        accumProb = accumProb + option.prob
        if(accumProb > u):
            return option
            # lstOption.remove(option)



def createPlan(listNodeUnschedule,lstRoute,gmaps,driver,db):
    #solution
    lstOption = []
    lstOption = upateF(listNodeUnschedule,lstRoute,lstOption,gmaps,driver,db)
    print("lstOption : ")
    print(lstOption)
    while len(lstOption)>0:
        option = selectOption(lstOption)
        print("do insert" + str(option))
        doInsert(lstRoute,option)
        lstOption = []
        listNodeUnschedule.remove(option.node)
        #update listOption
        #update listNodeUnschedule
        upateF(listNodeUnschedule,lstRoute,lstOption,gmaps,driver,db)
    return lstRoute

        
def doInsert(lstRoute,option):
    print(option.day)
    route = lstRoute[option.day]
    route[option.position : ] = option.route
           

def ration(route,node,i,gmaps,driver,db):
    
    # totalTimeNow = route['totalTime']
    # totalTimeAfter = totalTimeNow - fee(nodePre,nodePost) + fee(node,nodePost) + fee(nodePrev,node) + node['serviceTime'] 
    deltaTime = getFee(route[i-1],route[i],gmaps,driver,db) + getFee(node,route[i],gmaps,driver,db) + getFee(route[i-1],node,gmaps,driver,db) + node.serviceTime
    return node.score **2 / deltaTime

def getTotalScore(lstRoute):
    score = 0
    for route in lstRoute:
        for i in range(1,len(route)-1):
            score = score + route[i].score
    return score


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

def get_level(address_components,gmaps,db):
    result = {}
    i = 0
    for component in address_components:
        if 'administrative_area_level_1'  in component['types']:
            i += 1
            # print(component['long_name'])
            # print(address_components)
            ad1 = gmaps.geocode(component)
            # print(ad1)
            place_id = ad1[0]['place_id']
            name = db['region1_detail'].find_one({'place_id':place_id})['Ten tinh,thanh pho']
            result['administrative_area_level_1'] = name
        if ('locality' in component['types']) or ('administrative_area_level_2' in component['types']) or ('route' in component['types']) or ('sublocality_level_1'  in component['types']):
            i +=1
            result['level_'+str(i)] = component['long_name']
    return result

def fomat_text(text):
    for ch in ['\\','`','*','_','{','}','[',']','(',')','>','#','+','-','.','!','$','\''," ",',']:
        text = text.replace(ch,"")
    return text
def create_level(graphDB_Session,name,long_name,short_name,lat,lng,level,nameParent,levelParent):
    query_create  = ['CREATE (',"",":"+level+" { name:'","","',lat : ","",", lng:","",", long_name:'","","', short_name:'","","'})"]
    query_car  = ['CREATE (',"",":CarStation { name:'","","', long_name:'","","', short_name:'","","'})"]
    query_train  = ['CREATE (',"",":TrainStation { name:'","","', long_name:'","","', short_name:'","","'})"]
    query_plane  = ['CREATE (',"",":PlaneStation { name:'","","', long_name:'","","', short_name:'","","'})"]
    # query_car  = ['CREATE (',"",":BoardStation { name:'","","'})"]

    query_car_relation ="MATCH (a:"+level+"),(b:CarStation) WHERE a.name = \""+name+"\" and a.name = b.name CREATE (a)-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]->(b)"
    query_train_relation ="MATCH (a:"+level+"),(b:TrainStation) WHERE a.name = \""+name+"\" and  a.name = b.name CREATE (a)-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]->(b)"
    query_plane_relation ="MATCH (a:"+level+"),(b:PlaneStation) WHERE a.name = \""+name+"\" and  a.name = b.name CREATE (a)-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]->(b)"
    query_car1_relation ="MATCH (a:"+level+"),(b:CarStation) WHERE a.name = \""+name+"\" and  a.name = b.name CREATE (a)<-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]-(b)"
    query_train1_relation ="MATCH (a:"+level+"),(b:TrainStation) WHERE a.name = \""+name+"\" and a.name = b.name CREATE (a)<-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]-(b)"
    query_plane1_relation ="MATCH (a:"+level+"),(b:PlaneStation) WHERE a.name = \""+name+"\" and a.name = b.name CREATE (a)<-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]-(b)"
    query_parent_relation ="MATCH (a:"+levelParent+"),(b:"+level+") WHERE a.name ='"+nameParent+"' and b.long_name = '"+long_name+"' CREATE (a)-[r:child]->(b)"

    #1 :node, 3 : tên , 5 :lat , 7 :lng , 9 : long_name, 11: short_name
    query_create[1] = fomat_text(name)
    query_create[3] = name
    query_create[5] = lat 
    query_create[7] = lng
    query_create[9] = long_name
    query_create[11] = short_name

    query_car[1] = fomat_text(name)+'_car'
    query_car[3] = name
    query_car[5] = long_name
    query_car[7] = short_name

    query_train[1] = fomat_text(name)+'_train'
    query_train[3] = name       
    query_train[5] = long_name
    query_train[7] = short_name


    query_plane[1] = fomat_text(name)+'_plane'
    query_plane[3] = name
    query_plane[5] = long_name
    query_plane[7] = short_name

    # print(''.join(query_car))
    # print(''.join(query_create))

    # print(''.join(query_plane))

    graphDB_Session.run(''.join(query_create))

    graphDB_Session.run(''.join(query_plane))
    graphDB_Session.run(''.join(query_train))
    graphDB_Session.run(''.join(query_car))
    # print(query_car_relation)
    graphDB_Session.run(query_car_relation)
    graphDB_Session.run(query_car1_relation)
    graphDB_Session.run(query_train_relation)
    graphDB_Session.run(query_train1_relation)
    graphDB_Session.run(query_plane_relation)
    graphDB_Session.run(query_plane1_relation)
    # print(query_parent_relation)
    graphDB_Session.run(query_parent_relation)


def maxtrix_distance(lat,lng,mode,db,gmaps):
    #mode = 0 : car ; mode = 1 : 'plane' ; mode = 2 : train
    # car : 20 , plan :3 , train : 20
    db_collection = 'car_station_detail'
    i = 20
    name = 'dia chi'
    if(mode == 0):
        db_collection = 'car_station_detail'
        i = 50
        name = 'dia chi'
    if(mode == 1):
        db_collection = 'aiport_detail' 
        i  = 3
        name = 'MaSanBay'
    if(mode == 2):
        db_collection = 'train_staion_detail_final'
        i = 5
        name = 'Ten ga'
    listA = dict()
    listStation = list(db[db_collection].find({}))
    # print(len(listStation))
    for station in listStation:
        db[db_collection].update_one({name:station[name]},{'$set':  { "lat": station['Info'][0]['geometry']["location"]["lat"], "lng": station['Info'][0]['geometry']["location"]["lng"] }})
        listA[station[name]] = [station['Info'][0]['geometry']["location"]["lat"],station['Info'][0]['geometry']["location"]["lng"]]

    listA ={k: v for k, v in sorted(listA.items(), key=lambda x:  (x[1][0]-lat)**2 + (x[1][1]-lng)**2)}
    listlat = list(listA.values())
    listKey = list(listA.keys())[0:i]
    listDistance = []
    k = 0
    while(i>20):
        listDistance.extend(gmaps.distance_matrix([[lat,lng]],listlat[k*20:k*20+20])['rows'][0]['elements'])
        k = k+1
        i = i-20

    listDistance.extend(gmaps.distance_matrix([[lat,lng]],listlat[k*20:k*20+i])['rows'][0]['elements'])
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

    a = {'distance' : distances, "time" :time}
    return a


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
        query_plane_route1 = ["MATCH (a:PlaneStation {name:'","","'}),(b:Airport {code:\"","","\"}) CREATE (a)<-[r:route { min_price:","",", max_price :","",", ave_price :" ,"", ",min_time:","",", time : ","",", ave_time : ","",", type : 'driving'}]-(b)"]

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



# geocode_result = gmaps.geocode(m)
# db['test'].insert_one({'info':geocode_result})
# x = (get_level(reversed(geocode_result[0]['address_components']),gmaps,db))
# print(x)
# # match (lv1:administrative_area_level_1) -[:parent]-(lv2:lv2 {long_name :'HaNoi'}) return lv2

def insert_level(driver,gmaps,db,x):
    with driver.session() as graphDB_Session:
        listGeoCodeString = []
        y = {}
        y['administrative_area_level_1'] = x['administrative_area_level_1']
        geocode_string =  x['administrative_area_level_1']
        listGeoCodeString.append(geocode_string)
        query = "match (lv1:administrative_area_level_1 {name :'"+ x['administrative_area_level_1']+"'})"
        for i in range(2,len(x)+1):
            geocode_string = x['level_'+str(i)] +', '+ geocode_string
            listGeoCodeString.append(geocode_string)
            y['level_'+str(i)] = x['level_'+str(i)]
            query +=  "-[:child]->(lv"+str(i)+" :level_"+str(i)+" {name:'"+geocode_string+"'})"
            # print(query + "return lv"+str(i))
            results = graphDB_Session.run(query + "return lv"+str(i))
            records = []
            for record in results:
                records.append(record)
            # print("------------------"+str(len(records)))
            if(len(records) == 0):
                # print(geocode_string)
                info = gmaps.geocode(geocode_string)[0]
                long_name = info['address_components'][0]['long_name']
                short_name = info['address_components'][0]['short_name']
                lat = info['geometry']['location']['lat']
                lng = info['geometry']['location']['lng']
                car_distance = maxtrix_distance(lat,lng,0,db,gmaps)
                cost_car = {} 
                for key, value in car_distance['distance'].items():
                    cost_car[key] = taxi_fee(float(value))
                    cost_car = {k: v for k, v in sorted(cost_car.items(), key=lambda x: x[1])}

                train_distance = maxtrix_distance(lat,lng,2,db,gmaps)
                cost_train = {} 
                for key, value in train_distance['distance'].items():
                    cost_train[key] = taxi_fee(float(value))
                    cost_train = {k: v for k, v in sorted(cost_train.items(), key=lambda x: x[1])}

                plane_distance = maxtrix_distance(lat,lng,1,db,gmaps)
                cost_plane = {} 
                for key, value in plane_distance['distance'].items():
                    cost_plane[key] = taxi_fee(float(value))
                    cost_plane = {k: v for k, v in sorted(cost_plane.items(), key=lambda x: x[1])}
                db['level_'+str(i)].insert({'name': geocode_string, 'info' : info, 'long_name': geocode_string, ' short_name' : short_name, 'lat' : lat, 'lng':lng,'parent': y
                    ,'cost_car' : cost_car, 'time_car': car_distance['time'],'distance_car' : car_distance['distance'],
                    'cost_train' : cost_train, 'time_train': train_distance['time'],'distance_train' : train_distance['distance'],
                    'cost_plane' : cost_plane, 'time_plane': plane_distance['time'],'distance_plane' : plane_distance['distance']},check_keys=False)
                if(i == 2):
                    levelParent = 'administrative_area_level_1'
                else : 
                    levelParent = 'level_'+str(i-1)
                create_level(graphDB_Session,geocode_string,geocode_string,short_name,str(lat),str(lng),"level_"+str(i),listGeoCodeString[-2],levelParent)
                create_train_distance(graphDB_Session,geocode_string,cost_train,train_distance['time'])
                create_car_distance(graphDB_Session,geocode_string,cost_car,car_distance['time'])
                create_plane_distance(graphDB_Session,geocode_string,cost_plane,plane_distance['time'])
def query_route(typeTransport,WeightProperty,nameDeparture,levelDeparture,nameArrival,levelArrival,gmaps,graphDB_Session):
    nameType = 'TrainStation'
    if(typeTransport ==1) :
        nameType = 'TrainStation'
    if(typeTransport == 0):
        nameType = 'CarStation'
    if(typeTransport == 2):
        nameType ='PlaneStation' 

    query = ["MATCH (start:",nameType,"{name:\"", nameDeparture , "\"}), (end:" ,levelArrival,"{name:\"", nameArrival 
        ,"\"}) CALL algo.shortestPath.stream(start, end, \"" , WeightProperty,"\" ,{nodeQuery:' MATCH path=(a)-[:child*]->(:",levelDeparture,"{name : \"",nameDeparture,"\"}) WITH path MATCH (n) WHERE not n IN nodes(path) RETURN id(n) as id',relationshipQuery:'MATCH (n)-[r]->(m) where not (type(r) =\"child\") RETURN id(n) as source, id(m) as target, r.",WeightProperty," as weight',graph:'cypher'}) YIELD nodeId, cost  match (node) where id(node) = nodeId RETURN node.name AS name,nodeId, cost"]
    # print("".join(query))


    # query = ["MATCH (start:",nameType,"{name:\"", nameDeparture , "\"}), (end:" ,levelArrival,"{name:\"", nameArrival 
    #     ,"\"}) CALL algo.kShortestPaths.stream(start, end, 3, \"" , WeightProperty,"\" ,{nodeQuery:'MATCH (n) WHERE not(labels(n) = [\"",levelDeparture,"\"] and n.name = \"",nameDeparture,"\") RETURN id(n) as id',relationshipQuery:'MATCH (n)-[r]->(m) RETURN id(n) as source, id(m) as target, r.",WeightProperty," as weight',graph:'cypher'}) YIELD index, nodeIds, costs RETURN [node in algo.getNodesById(nodeIds) | node.name] AS places,nodeIds,costs,reduce(acc = 0.0, cost in costs | acc + cost) AS totalCost"]
    # print("".join(query))
    results = graphDB_Session.run("".join(query))

    records = []
    for record in results:
        records.append(record)
    # print(records)
# MATCH (a)-[r]->(b) where id(a) = 562 and id(b) = 127 return r
    if (len(records)>0):
        fistNode = records[1]['nodeId']
        lastNode = records[-3]['nodeId']
        # print(fistNode)
        #get info lastnode and first node
        node_info = {}
        node_info_in_path = graphDB_Session.run("MATCH (a),(b) where id(a) = " +str(fistNode)+" and id(b) = "+str(lastNode)+" return a.lat as firstLat, a.lng as firstLng,b.lat as lastLat, b.lng as lastLng ")
        for _ in node_info_in_path:
            # print(_['k'])
            node_info['firstLat'] = _['firstLat']
            node_info['lastLat'] = _['lastLat']
            node_info['firstLng'] = _['firstLng']
            node_info['lastLng'] = _['lastLng']

        listway = []

        #get info path
        for i in range(len(records)-1):
            a = records[i]['nodeId']
            b = records[i+1]['nodeId']
            way_info = graphDB_Session.run("MATCH (a)-[r]->(b) where id(a) = " +str(a)+" and id(b) = "+str(b)+" return r.type,r."+WeightProperty+" as cost, TYPE(r) as k,a.lat as latDeparture,a.lng as lngDeparture,b.lat as latArrival,b.lng as lngArrival")
            info = {}
            for _ in way_info:
                # print(_['k'])
                info['type'] = _['r.type']
                # print(info)
                info[WeightProperty] = _['cost']

                # latDeparture,a.lng as lngDeparture,b.lat as latArrival,b.lng as lngArrival
                info['latDeparture'] = _['latDeparture']
                info['lngDeparture'] = _['lngDeparture']
                info['latArrival'] = _['latArrival']
                info['lngArrival'] = _['lngArrival']
            way  = {
                "Departure" : records[i]['name'],
                "Arrival" : records[i+1]['name'],
                "type" :  info['type'],
                "cost" : info[WeightProperty],
                'latDeparture' :  info['latDeparture'] ,
                'lngDeparture' : info['lngDeparture'] ,
                'latArrival':info['latArrival'] ,
                'lngArrival': info['lngArrival'] 
            }
            if(way['cost'] != 0):
                listway.append(way)
        # if (len(listway)>0):
        listWay1 = []
        listWay1.append(listway[0])
        listWay1.append(listway[-1])

        for i in range(1,len(listway)-1):
            if(listway[i-1]['type']== 'driving' and listway[i+1]['type']== 'driving'):
                if(listway[i]['type']== 'driving' ):
                    continue
                else:
                    listWay1.insert(-1,listway[i])    
            else:
                listWay1.insert(-1,listway[i])
        # print("----------------list1------------------")
        # print(listWay1)

        listWayFinal = []
        for i in range(len(listWay1)-1):
            # print (i)
            if(listWay1[i]['type'] == 'driving'):
                if (listWay1[i+1]['type'] != 'driving'):
                    listWayFinal.append(listWay1[i])
                else :
                    # print("dfđ")
                    # print(listway[i])

                    # print(listway[i+1])
                    listWay1[i+1]['Departure'] = listWay1[i]['Departure']
                    listWay1[i+1]['latDeparture'] = listWay1[i]['latDeparture']
                    listWay1[i+1]['lngDeparture'] = listWay1[i]['lngDeparture']
                    # print(listWay1[i])
                    # listWayFinal.append(listWay1[i])
                    # # i = i+1
                    # continue
            else:
                listWayFinal.append(listWay1[i])
        listWayFinal.append(listWay1[-1])
        # print("----------------listFinal------------------")
        # print(listWayFinal)

        return {'way' : listWayFinal , 'node_info': None}
    else :
        return None
# with driver.session() as graphDB_Session:
#     query_route(1,'ave_price','Thành phố Vinh, Nghệ An','level_2','Hà Nội','administrative_area_level_1',gmaps,graphDB_Session)

def find_route(departure,arrival,gmaps,driver,db): 

    m1 = departure
    m2 = arrival
    geocode_result1 = gmaps.geocode(m1)
    geocode_result2 = gmaps.geocode(m2)
    # print(geocode_result2)
    # db['test'].insert_one({'info':geocode_result})
    depart_level = (get_level(reversed(geocode_result1[0]['address_components']),gmaps,db))
    arrival_level = (get_level(reversed(geocode_result2[0]['address_components']),gmaps,db))
    # print(depart_level.keys())
    nameDeparture = ", ".join(reversed(list(depart_level.values())))
    levelDeparture = list(depart_level.keys())[-1]
    nameArrival = ", ".join(reversed(list(arrival_level.values())))
    levelArrival = list(arrival_level.keys())[-1]

    # print ( nameDeparture + "-=------" +levelDeparture )
    # print ( nameArrival + "-=------" +levelArrival )
    insert_level(driver,gmaps,db,depart_level)
    insert_level(driver,gmaps,db,arrival_level)
    with driver.session() as graphDB_Session:
        way = query_route(1,'min_time',nameDeparture,levelDeparture,nameArrival,levelArrival,gmaps,graphDB_Session)
        if way != None:
            # print(way)
            a = [geocode_result1[0]['geometry']['location']['lat'],geocode_result1[0]['geometry']['location']['lng']]
            b = [way['way'][0]['latDeparture'],way['way'][0]['lngDeparture']]
            # print(a)
            # print(b)
            # if(len(way['way'])>1):
            # start = gmaps.distance_matrix([a],[b])
            # print(start)
            # start_detail['departure'] = nameDeparture
            # start_detail['arrival'] = way[0]['departure']
            # end = gmaps.distance_matrix([[way['way'][-1]['latDeparture'],way['way'][-1]['lngDeparture']]],[[geocode_result2[0]['geometry']['location']['lat'],geocode_result2[0]['geometry']['location']['lng']]])
            # db['test'].insert_one({'info': start})
            # if()
            way['way'][0]['Departure'] = m1
            way['way'][0]['latDeparture'] = geocode_result1[0]['geometry']['location']['lat']
            way['way'][0]['lngDeparture'] = geocode_result1[0]['geometry']['location']['lng']
            # way['way'][0]['cost'] = start['rows'][0]['elements'][0]['duration']['value']
            way['way'][-1]['Arrival'] = m2
            way['way'][-1]['latArrival'] = geocode_result2[0]['geometry']['location']['lat']
            way['way'][-1]['lngArrival'] = geocode_result2[0]['geometry']['location']['lng']
            # way['way'][-1]['cost'] = end['rows'][0]['elements'][0]['duration']['value']
            ways = way['way']
            # for i in range []
            # for i in range(0,len(ways)):
            #     if(ways[i]['type']) == 'driving':
            #         depart = ways[i]['Departure']
            #         while(ways[i+1]['type'] == 'driving'):
            #             i = i+1
            #         arrival = ways[i]['Arrival']
            totalCost = 0
            for w in way['way']:
                if(w['type'] == 'driving'):
                    info_cost =  gmaps.distance_matrix([[w['latDeparture'],w['lngDeparture']]],[[w['latArrival'],w['lngArrival']]])
                    w['cost'] = info_cost['rows'][0]['elements'][0]['duration']['value']
                    totalCost  = totalCost + w['cost']
                        # totalCost = 0
                else:
                    totalCost  = totalCost + w['cost']
                
            return totalCost
        else :
            a = [geocode_result1[0]['geometry']['location']['lat'],geocode_result1[0]['geometry']['location']['lng']]
            b = [geocode_result2[0]['geometry']['location']['lat'],geocode_result2[0]['geometry']['location']['lng']]

            # gmaps.distance_matrix([[w['latDeparture'],w['lngDeparture']]],[[w['latArrival'],w['lngArrival']]])
            #         w['cost'] = info_cost['rows'][0]['elements'][0]['duration']['value']
            return gmaps.distance_matrix([a],[b])['rows'][0]['elements'][0]['duration']['value']


# def shake(listNodeUnschedule, route, cons,post):
# 	S += 1
# 	for l in range(S,S+R):
# 		ln_loc = len(Locations) 
# 		i = 1 if l >= (ln_loc-1) else l
# 		if ln_loc > 2 and i < (ln_loc-1) and i > 0 :

# 			if Locations[i].name.lower() != "end" or Locations[i].name.lower() != "start":
# 				RestOfLocations.append( Locations[i] )

# 			Locations.remove( Locations[i] )

# 	return Locations

if __name__ == "__main__":
    mongo_uri = 'mongodb://localhost:27017'
    mongo_db = 'DataTransport'


    # gmaps = googlemaps.Client(key='AIzaSyD4QbuZzxKOyrBIw-LfVe31n38pxSSd2co')
    # gmaps = googlemaps.Client(key='AIzaSyCbhGuXbFO7RvpyYPCeZWlkzzTE2rBZbYc')

    gmaps = googlemaps.Client(key='AIzaSyD4n_B9MKx7XooJ6kaXkLFe-JMPhkVMsGg')

    listNodeUnschedule = []

    numberDay = 4

    lstOption = []
    client = MongoClient(mongo_uri)
    db = client[mongo_db]

    uri = "bolt://localhost"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "123a!@#A"))
    dpt = Node(1,21600,50,60,"22 lê khôi, Vinh, Nghệ An")
    arv = Node(1,20,50,60,"Đại học Bách Khoa Hà Nội")
    a = Node(1,25200,28000,300,"43 chùa bộc, đống đa, hà nội")
    b = Node(1,25200,28000,300,"cảng hàng không Vinh")
    c = Node(1,28000,32000,300,"bến xe mỹ đình")
    d = Node(1,26000,40000,300,"ga hà nội")
    e = Node(1,45200,50000,300,"lăng bác")

    listNodeUnschedule =  [a,b,c,d,e]

# nodePost.earliestTime - node.serviceTime - getFee(node,nodePost,gmaps,driver,db)> node.earliestTime and   node.earliestTime > nodePrev.earliestTime + nodePrev.serviceTime + getFee(nodePrev,node,gmaps,driver,db)):

    listRoute = [[Node(1,21600,21600,0,"22 lê khôi, Vinh, Nghệ An"),Node(1,576000,576000,0,"Đại học Bách Khoa Hà Nội")],[Node(1,21600,21600,0,"Đại học Bách Khoa Hà Nội"),Node(1,576000,576000,0,"22 lê khôi, Vinh, Nghệ An")]]
    # print(getFee(dpt,arv,gmaps,driver,db))
    print('result')
    from copy import deepcopy
    firstSolution = createPlan(listNodeUnschedule,deepcopy(listRoute),gmaps,driver,db)
    print("listNodeUnschedule")
    for _ in listNodeUnschedule:
        print(str(_))
    for route in firstSolution:
        if(len(route)>=3):
            print("unschedule element")
            for i in range(1,len(route)-1):
                print(str(route[i]))
                listNodeUnschedule.append(route[i])

    print("listNodeUnschedule")
    for _ in listNodeUnschedule:
        print(str(_))
    secondSolution = createPlan(deepcopy(listNodeUnschedule),deepcopy(listRoute),gmaps,driver,db)

    bestSolution = firstSolution if getTotalScore(firstSolution) >= getTotalScore(secondSolution) else secondSolution
    # while (no_improve <5):

    #     createPlan(listNodeUnschedule,listRoute,gmaps,driver,db)

    for route in bestSolution:
        for n in route:
            print("------------------------------")
            print(str(n))