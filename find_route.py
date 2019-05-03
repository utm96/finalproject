from neo4j import GraphDatabase
from pymongo import MongoClient


uri = "bolt://localhost"
driver = GraphDatabase.driver(uri, auth=("neo4j", "123a!@#A"))

CITY = ["Vinh - Nghệ An","Hà Nội","Hải Phòng","Cần Thơ","Vũng Tàu - Bà Rịa-Vũng Tàu","Hồ Chí Minh","Đà Nẵng","Huế - Thừa Thiên-Huế"]
with driver.session() as graphDB_Session:
# CQL to create a graph containing some of the Ivy League universities
    # for c in CITY:
    #     c = c.replace(' ','')
    # a = input("nhap thong tin diem xuat phat: ")
    # b = input("nhap thong tin diem den: ")
    a = 'Hà Nội'
    b = 'Hồ Chí Minh'
    cqlCreate = "MATCH (start:city{name:\'"+a+"\'}), (end:city{name:\'"+b+"\'}) CALL algo.kShortestPaths.stream(start, end, 3, 'min_price' ,{direction: 'OUTGOING'}) YIELD  nodeIds, costs RETURN [node in algo.getNodesById(nodeIds) | node.name] AS places, costs, reduce(acc = 0.0, cost in costs | acc + cost) AS totalCost "
    # cqlCreate = "MATCH (x:city) RETURN x"
    tx = graphDB_Session.run(cqlCreate)
    result = []
    for record in tx:
        listPlace = record['places']
        listType = []
        for i in range(len(listPlace)-1):
            print(listPlace[i] + "-------------" + listPlace[i+1])
            cqlTransport = "MATCH (x:city {name:\'"+listPlace[i]+"\'})-[r]->(y:city {name :\'"+ listPlace[i+1]+"\'}) RETURN r.type"
            typeTransport = graphDB_Session.run(cqlTransport)
            for _ in typeTransport:
                listType.append(_['r.type'])
        result.append({
            'places': record['places'],
            'costs' : record['costs'],
            'total_cost': record['totalCost'],
            'listTransport': listType
        })

    print(result)
        # print(record['places'])
        # print(record["costs"])
    # graphDB_Session.close()

