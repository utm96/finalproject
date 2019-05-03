from neo4j import GraphDatabase
from pymongo import MongoClient


uri = "bolt://localhost"
driver = GraphDatabase.driver(uri, auth=("neo4j", "123a!@#A"))

CITY = ["Vinh - Nghệ An","Hà Nội","Hải Phòng","Cần Thơ","Vũng Tàu - Bà Rịa-Vũng Tàu","Hồ Chí Minh","Đà Nẵng","Huế - Thừa Thiên-Huế"]

mongo_uri = 'mongodb://localhost:27017'
mongo_db = 'DataTransport'
client = MongoClient(mongo_uri)
db = client[mongo_db]


with driver.session() as graphDB_Session:
# CQL to create a graph containing some of the Ivy League universities
    # for c in CITY:
    #     c = c.replace(' ','')

    for fromSource in CITY:
        location = db['car_station'].find_one({"value": fromSource})
        fromStateId = location['StateId']
        fromCityId = location['CityId']
        codeFrom = ''
        if(fromCityId == 0):
            codeFrom = 's'+ str(fromStateId)

        else:
            codeFrom = 'c'+ str(fromCityId) 
        
        cqlCreate = "CREATE ("+codeFrom+":city { name: \'"+fromSource+"\'})"
        graphDB_Session.run(cqlCreate)


    for fromSource in CITY:
        location = db['car_station'].find_one({"value": fromSource})
        fromStateId = location['StateId']
        fromCityId = location['CityId']
        codeFrom = ''
        codeFrom1 = ''
        if(fromCityId == 0):
            codeFrom = '1'+ str(fromStateId)
            codeFrom1 = 's'+ str(fromStateId)

        else:
            codeFrom = '2'+ str(fromCityId) 
            codeFrom1 = 'c'+ str(fromStateId)

        # cqlCreate = "CREATE ("+codeFrom+":city { name: \'"+fromSource+"\'})"
        # graphDB_Session.run(cqlCreate)

        for toDest in CITY:
            if(toDest != fromSource):
                dest = db['car_station'].find_one({"value": toDest})
                toStateId = dest['StateId']
                toCityId = dest['CityId']
                codeTo = ''
                codeTo1 = ''
                if(toCityId == 0):
                    codeTo = '1'+ str(toStateId)  + '1'
                    codeTo1 = 's'+ str(toStateId) 
                else:
                    codeTo = '2'+str(toCityId) + '1'
                    codeTo1 = 'c'+ str(toStateId) 
                code = codeFrom + 't' + codeTo

                prices = []
                car_price = db['car_detail'].find_one({"code": code})
                if(car_price != None):
                    prices.append({'price' : car_price['average'],'type': 'car'})
                plane_price = db['plane_detail'].find_one({"code": code})
                if(plane_price != None):
                    prices.append({'price' : plane_price['average'],'type': 'plane'})
                train_price = db['train_detail'].find_one({"code": code})
                if(train_price != None):
                    prices.append({'price' : train_price['average'],'type': 'train'})
                if(len(prices)>0):
                    minPricedItem = min(prices, key=lambda x:x['price'])
                    # MATCH (a:Person),(b:Person)
                    # WHERE a.name = 'A' AND b.name = 'B'
                    # CREATE (a)-[r:RELTYPE]->(b)
                    # RETURN type(r)
                    cql =     "MATCH (a:city),(b:city)"+"WHERE a.name = \'"+fromSource+"\' AND b.name = \'"+toDest+"\' CREATE (a)-[:goTo {min_price:"+ str(minPricedItem['price']) +", type :\'"+minPricedItem['type'] +"\' }]->(b)"
                    graphDB_Session.run(cql)

                    
# MATCH (start:city{name:'Vinh - Nghệ An'}), (end:city{name:'Hải Phòng'})
# CALL algo.kShortestPaths.stream(start, end, 3, 'min_price' ,{})
# YIELD  nodeIds, costs
# RETURN [node in algo.getNodesById(nodeIds) | node.name] AS places,
#        costs,
#        reduce(acc = 0.0, cost in costs | acc + cost) AS totalCost