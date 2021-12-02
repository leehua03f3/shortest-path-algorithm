import csv
import datetime

# This class defines Package object that includes information of a package
class Package:
    # The information includes: package id, address, city, state, zipcode, deadline, and mass
    def __init__(self, id, address, city, state, zipcode, deadline, mass):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = self.convertTime(deadline)
        self.mass = mass
        self.status = "At Hub"
        self.deliveryTime = datetime.timedelta(hours=8)

    # This function returns the string version of the Package object
    def __str__(self):  # overwite print(Package) otherwise it will print object reference
        return "%s, %s, %s, %s, %s, %s, %s" % (
        self.id, self.address, self.city, self.state, self.zipcode, self.deadline, self.mass)

    # This function sets status for the instance
    def setStatus (self, status):
        self.status = status

    # This function sets delivery time for the instance
    def setDeliveryTime(self, time):
        self.deliveryTime = time

    # This function converts string to Time object
    def convertTime(self, time):
        if time == "EOD":
            convertedTime = datetime.time(23,59,59)
            # print(convertedTime)
        else:
            time = time.split(':')
            convertedTime = datetime.time(int(time[0]), int(time[1][:2]), 00)
            # print(convertedTime)
        return convertedTime

# This functions loads information of the package from .csv file to the Hash Table
def loadPackages(fileName, hashTable):
    with open(fileName) as package:
        packageData = csv.reader(package, delimiter=',')
        next(packageData)  # skip header
        for data in packageData:
            id = int(data[0])
            address = " " + data[1]
            city = data[2]
            state = data[3]
            zipcode = data[4]
            deadline = data[5]
            mass = int(data[6])

            p = Package(id, address, city, state, zipcode, deadline, mass)

            # Insert it into the hash table
            hashTable.insert(id, p)

# This class defines the Graph object
class Graph:
    def __init__(self):
        self.connections = {}

    # This functions sets the distance from two address
    def setDistance(self, from_vertex, to_vertex, distance):
        self.connections[(from_vertex, to_vertex)] = distance

# This functions loads distances between addresses from CSV file to a Graph
def loadDistance(fileName):
    g = Graph()

    with open("data/WGUPS Distance Table.csv", 'r') as file:
        distanceData = csv.reader(file, delimiter=',')
        next(distanceData)
        for data in distanceData:
            g.setDistance(data[0], data[1], float(data[2]))
            g.setDistance(data[1], data[0], float(data[2]))

    return g;