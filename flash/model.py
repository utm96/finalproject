import json

class Node:
    def __init__(self,score,earliestTime,lastestTime,serviceTime,address):
        self.score = score
        self.earliestTime = earliestTime
        self.lastestTime = lastestTime
        self.serviceTime = serviceTime
        self.address = address
        self.startTime = self.earliestTime
        self.endTime = self.startTime + self.serviceTime
        self.fee = {}
    def setFee (self,fee):
        self.feeToNext = fee 
    def distance(self,fee,id):
        self.fee[id] = fee
    def  __str__(self):
        return self.address +","+str(self.startTime) + "," + str(self.endTime) + ", lastestTime : " +str(self.lastestTime) + ", len fee: " + str(len(self.fee))
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class UsePlan:
    def __init__(self,dayRoutes):
        self.dayRoutes = dayRoutes


class DayRoute:
    def __init__(self, startTime, endTime, startNode, endNode,totalCost):
        self.startTime = startTime
        self.endTime = endTime
        self.dayPlan = [startNode,endNode]
        
    def addLocation(self,node,i):
        self.dayPlan.insert(i,node)

class Option:
    def __init__(self, day, position, node, sumRation, prob,route):
        self.day = day
        self.position = position
        self.node = node 
        self.sumRation = sumRation
        self.prob = prob
        self.route = route
    def  __str__(self):
        return self.node.address + str(self.day) + " ration : " + str(self.sumRation)
