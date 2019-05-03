from neo4j import GraphDatabase
from pymongo import MongoClient

            # data_plane = {"project":"scraper","spider":"plane_detail","url":plane_data,'code':code,"depart":fromSource,"dest":toDest}
            # url = 'http://127.0.0.1:6800/schedule.json'
            # req_car = grequests.post(url,data=data_car)

# MATCH (a:administrative_area_level_1),(b:CarStation) WHERE a.name = b.name CREATE (a)-[r:route { min_price: 0, price = 0, ave_price = 0 ,min_time: 0, time = 0, ave_time = 0 }]->(b)


uri = "bolt://localhost"
driver = GraphDatabase.driver(uri, auth=("neo4j", "123a!@#A"))
mongo_uri = 'mongodb://localhost:27017'
mongo_db = 'DataTransport'
client = MongoClient(mongo_uri)
db = client[mongo_db]
# x = requests.post(url,data=j)
# print(x)
regions = list(db['region1_detail'].find({}))

print(len(regions))
    #    "location": {
    #       "lat": 10.5417397,
    #       "lng": 107.2429976
    #     },
    # 'CREATE ('Ha noi'):administrative_area_level_1 { name:'hà nội',lat : 10.5417397, lng: 107.2429976}]
        #       "long_name": "Ba Ria - Vung Tau",
        #   "short_name": "Ba Ria - Vung Tau",
query_create  = ['CREATE (',"",":administrative_area_level_1 { name:'","","',lat : ","",", lng:","",", long_name:'","","', short_name:'","","'})"]
query_car  = ['CREATE (',"",":CarStation { name:'","","', long_name:'","","', short_name:'","","'})"]
query_train  = ['CREATE (',"",":TrainStation { name:'","","', long_name:'","","', short_name:'","","'})"]
query_plane  = ['CREATE (',"",":PlaneStation { name:'","","', long_name:'","","', short_name:'","","'})"]
# query_car  = ['CREATE (',"",":BoardStation { name:'","","'})"]

query_car_relation ="MATCH (a:administrative_area_level_1),(b:CarStation) WHERE a.name = b.name CREATE (a)-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0, hop:5 }]->(b)"
query_train_relation ="MATCH (a:administrative_area_level_1),(b:TrainStation) WHERE a.name = b.name CREATE (a)-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0, hop:5  }]->(b)"
query_plane_relation ="MATCH (a:administrative_area_level_1),(b:PlaneStation) WHERE a.name = b.name CREATE (a)-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 , hop:5 }]->(b)"
query_car1_relation ="MATCH (a:administrative_area_level_1),(b:CarStation) WHERE a.name = b.name CREATE (a)<-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 , hop:5 }]-(b)"
query_train1_relation ="MATCH (a:administrative_area_level_1),(b:TrainStation) WHERE a.name = b.name CREATE (a)<-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 , hop:5 }]-(b)"
query_plane1_relation ="MATCH (a:administrative_area_level_1),(b:PlaneStation) WHERE a.name = b.name CREATE (a)<-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 , hop:5 }]-(b)"

#1 :node, 3 : tên , 5 :lat , 7 :lng , 9 : long_name, 11: short_name
with driver.session() as graphDB_Session:
    for region in regions:
        query_create[1] = region['Info'][0]['address_components'][0]['long_name'].replace(" ","").replace("-","_")
        query_create[3] = region['Ten tinh,thanh pho']
        query_create[5] = str(region['Info'][0]['geometry']['location']['lat']) 
        query_create[7] = str(region['Info'][0]['geometry']['location']['lng'])
        query_create[9] = region['Info'][0]['address_components'][0]['long_name']
        query_create[11] = region['Info'][0]['address_components'][0]['short_name']

        query_car[1] = region['Info'][0]['address_components'][0]['long_name'].replace(" ","").replace("-","_")+'_car'
        query_car[3] = region['Ten tinh,thanh pho']
        query_car[5] = region['Info'][0]['address_components'][0]['long_name']
        query_car[7] = region['Info'][0]['address_components'][0]['short_name']

        query_train[1] = region['Info'][0]['address_components'][0]['long_name'].replace(" ","").replace("-","_")+'_train'
        query_train[3] = region['Ten tinh,thanh pho']        
        query_train[5] = region['Info'][0]['address_components'][0]['long_name']
        query_train[7] = region['Info'][0]['address_components'][0]['short_name']


        query_plane[1] = region['Info'][0]['address_components'][0]['long_name'].replace(" ","").replace("-","_")+'_plane'
        query_plane[3] = region['Ten tinh,thanh pho']
        query_plane[5] = region['Info'][0]['address_components'][0]['long_name']
        query_plane[7] = region['Info'][0]['address_components'][0]['short_name']

        print(''.join(query_car))
        graphDB_Session.run(''.join(query_create))

        graphDB_Session.run(''.join(query_plane))
        graphDB_Session.run(''.join(query_train))
        graphDB_Session.run(''.join(query_car))
    graphDB_Session.run(query_car_relation)
    graphDB_Session.run(query_car1_relation)
    graphDB_Session.run(query_train_relation)
    graphDB_Session.run(query_train1_relation)
    graphDB_Session.run(query_plane_relation)
    graphDB_Session.run(query_plane1_relation)

# CQL to create a graph containing some of the Ivy League universities
    # for c in CITY:
    #     c = c.replace(' ','')

    # for region in regions:
        
    #     location = db['car_station'].find_one({"value": fromSource})
    #     fromStateId = location['StateId']
    #     fromCityId = location['CityId']
    #     codeFrom = ''
    #     if(fromCityId == 0):
    #         codeFrom = 's'+ str(fromStateId)

    #     else:
    #         codeFrom = 'c'+ str(fromCityId) 
        
    #     cqlCreate = "CREATE ("+codeFrom+":city { name: \'"+fromSource+"\'})"
    #     graphDB_Session.run(cqlCreate)


    # for fromSource in CITY:
    #     location = db['car_station'].find_one({"value": fromSource})
    #     fromStateId = location['StateId']
    #     fromCityId = location['CityId']
    #     codeFrom = ''
    #     codeFrom1 = ''
    #     if(fromCityId == 0):
    #         codeFrom = '1'+ str(fromStateId)
    #         codeFrom1 = 's'+ str(fromStateId)

    #     else:
    #         codeFrom = '2'+ str(fromCityId) 
    #         codeFrom1 = 'c'+ str(fromStateId)

    #     # cqlCreate = "CREATE ("+codeFrom+":city { name: \'"+fromSource+"\'})"
    #     # graphDB_Session.run(cqlCreate)

    #     for toDest in CITY:
    #         if(toDest != fromSource):
    #             dest = db['car_station'].find_one({"value": toDest})
    #             toStateId = dest['StateId']
    #             toCityId = dest['CityId']
    #             codeTo = ''
    #             codeTo1 = ''
    #             if(toCityId == 0):
    #                 codeTo = '1'+ str(toStateId)  + '1'
    #                 codeTo1 = 's'+ str(toStateId) 
    #             else:
    #                 codeTo = '2'+str(toCityId) + '1'
    #                 codeTo1 = 'c'+ str(toStateId) 
    #             code = codeFrom + 't' + codeTo

    #             prices = []
    #             car_price = db['car_detail'].find_one({"code": code})
    #             if(car_price != None):
    #                 prices.append({'price' : car_price['average'],'type': 'car'})
    #             plane_price = db['plane_detail'].find_one({"code": code})
    #             if(plane_price != None):
    #                 prices.append({'price' : plane_price['average'],'type': 'plane'})
    #             train_price = db['train_detail'].find_one({"code": code})
    #             if(train_price != None):
    #                 prices.append({'price' : train_price['average'],'type': 'train'})
    #             if(len(prices)>0):
    #                 minPricedItem = min(prices, key=lambda x:x['price'])
    #                 # MATCH (a:Person),(b:Person)
    #                 # WHERE a.name = 'A' AND b.name = 'B'
    #                 # CREATE (a)-[r:RELTYPE]->(b)
    #                 # RETURN type(r)
    #                 cql =     "MATCH (a:city),(b:city)"+"WHERE a.name = \'"+fromSource+"\' AND b.name = \'"+toDest+"\' CREATE (a)-[:goTo {min_price:"+ str(minPricedItem['price']) +", type :\'"+minPricedItem['type'] +"\' }]->(b)"
    #                 graphDB_Session.run(cql)

                    
# MATCH (start:city{name:'Vinh - Nghệ An'}), (end:city{name:'Hải Phòng'})
# CALL algo.kShortestPaths.stream(start, end, 3, 'min_price' ,{})
# YIELD  nodeIds, costs
# RETURN [node in algo.getNodesById(nodeIds) | node.name] AS places,
#        costs,        # reduce(acc = 0.0, cost in costs | acc + cost) AS totalCost