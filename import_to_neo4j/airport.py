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
airports = list(db['aiport_detail'].find({}))

print(len(airports))
    #    "location": {
    #       "lat": 10.5417397,
    #       "lng": 107.2429976
    #     },
    # 'CREATE ('Ha noi'):administrative_area_level_1 { name:'hà nội',lat : 10.5417397, lng: 107.2429976}]
query_create  = ['CREATE (',"",":Airport { name:'","","',lat : ","",", lng:","",", code:'","","'})"]
# query_car  = ['CREATE (',"",":CarStation { name:'","","'})"]
# query_train  = ['CREATE (',"",":TrainStop { name:'","","'})"]
# query_plane  = ['CREATE (',"",":PlaneStation { name:'","","'})"]
# query_car  = ['CREATE (',"",":BoardStation { name:'","","'})"]

# query_car_relation ="MATCH (a:administrative_area_level_1),(b:CarStation) WHERE a.name = b.name CREATE (a)-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]->(b)"
# query_train_relation ="MATCH (a:administrative_area_level_1),(b:TrainStation) WHERE a.name = b.name CREATE (a)-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]->(b)"
# query_plane_relation ="MATCH (a:administrative_area_level_1),(b:PlaneStation) WHERE a.name = b.name CREATE (a)-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]->(b)"
# query_car1_relation ="MATCH (a:administrative_area_level_1),(b:CarStation) WHERE a.name = b.name CREATE (a)<-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]-(b)"
# query_train1_relation ="MATCH (a:administrative_area_level_1),(b:TrainStation) WHERE a.name = b.name CREATE (a)<-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]-(b)"
# query_plane1_relation ="MATCH (a:administrative_area_level_1),(b:PlaneStation) WHERE a.name = b.name CREATE (a)<-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]-(b)"

#1 :node, 3 : tên , 5 :lat , 7 :lng , 9: code
with driver.session() as graphDB_Session:
    for airport in airports:
        query_create[1] = airport['MaSanBay'].replace(" ","").replace("-","_")
        query_create[3] = airport['Ten san bay']
        print(airport['Ten san bay'])
        query_create[5] = str(airport['Info'][0]['geometry']['location']['lat']) 
        query_create[7] = str(airport['Info'][0]['geometry']['location']['lng'])
        query_create[9] = airport['MaSanBay'].replace(" ","").replace("-","_")

    #     query_car[1] = region['Info'][0]['address_components'][0]['long_name'].replace(" ","").replace("-","_")+'_car'
    #     query_car[3] = region['Ten tinh,thanh pho']
    #     query_train[1] = region['Info'][0]['address_components'][0]['long_name'].replace(" ","").replace("-","_")+'_train'
    #     query_train[3] = region['Ten tinh,thanh pho']        
    #     query_plane[1] = region['Info'][0]['address_components'][0]['long_name'].replace(" ","").replace("-","_")+'_plane'
    #     query_plane[3] = region['Ten tinh,thanh pho']
    #     # print(''.join(query_car))
        graphDB_Session.run(''.join(query_create))

    #     graphDB_Session.run(''.join(query_plane))
    #     graphDB_Session.run(''.join(query_train))
    #     graphDB_Session.run(''.join(query_car))
    # graphDB_Session.run(query_car_relation)
    # graphDB_Session.run(query_car1_relation)
    # graphDB_Session.run(query_train_relation)
    # graphDB_Session.run(query_train1_relation)
    # graphDB_Session.run(query_plane_relation)
    # graphDB_Session.run(query_plane1_relation)

