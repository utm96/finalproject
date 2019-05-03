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

# query_car_relation ="MATCH (a:administrative_area_level_1),(b:CarStation) WHERE a.name = b.name CREATE (a)-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]->(b)"
# query_train_relation ="MATCH (a:administrative_area_level_1),(b:TrainStation) WHERE a.name = b.name CREATE (a)-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]->(b)"
# query_plane_relation ="MATCH (a:administrative_area_level_1),(b:PlaneStation) WHERE a.name = b.name CREATE (a)-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]->(b)"
# query_car1_relation ="MATCH (a:administrative_area_level_1),(b:CarStation) WHERE a.name = b.name CREATE (a)<-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]-(b)"
# query_train1_relation ="MATCH (a:administrative_area_level_1),(b:TrainStation) WHERE a.name = b.name CREATE (a)<-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]-(b)"
# query_plane1_relation ="MATCH (a:administrative_area_level_1{name : \""++"\"}) set a.place_id = \"""\""

#1 :node, 3 : tên , 5 :lat , 7 :lng , 9 : long_name, 11: short_name
with driver.session() as graphDB_Session:
    for region in regions:
        query = "MATCH (a:administrative_area_level_1{name : \""+region['Ten tinh,thanh pho']+"\"}) set a.place_id = \""+region['Info'][0]['place_id']+"\""
        print(query)
        graphDB_Session.run(query)