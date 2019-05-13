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
routes = list(db['car_route_detail_final'].find({}))

print(len(routes))

query_car_route = ["MATCH (a:CarStop {address:\"","","\"}),(b:CarStop {address:\"","","\"}) CREATE (a)-[r:route { min_price:","",", max_price :","",", ave_price :" ,"", ",min_time:","",", time : ","",", ave_time : ","",", type : 'car',hop:1, price :","","}]->(b)"]
#1 :code1, 3 : code2 , 5 :min_price , 7 :max_price,9 :ave_price, 11 :min_time , 13: time , 15 : ave_time
with driver.session() as graphDB_Session:
    for route in routes:

        query_car_route[1] = route['departure']
        query_car_route[3] = route['arrival']
        query_car_route[5] = str(route['price'])
        query_car_route[7] = str(route['price'])
        query_car_route[9] = str(route['price'])
        query_car_route[11] = str(route['time']*60)
        query_car_route[13] = str(route['time']*60)
        query_car_route[15] = str(route['time']*60)
        query_car_route[17] = str(route['price'])

        # print(''.join(query_car_route))
        graphDB_Session.run(''.join(query_car_route))
