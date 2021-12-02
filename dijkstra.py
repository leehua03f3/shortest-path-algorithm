from loadData import Graph
import loadData
import datetime
from chainingHashTable import ChainingHashTable

# Condition for all the packages
packageBefore1030 = [1, 13, 14, 16, 20, 29, 30, 31, 34, 37, 40]
packageGoTogether = [13, 14, 15, 16, 19, 20]
packageGoToTruck2 = [3, 18, 36, 38]
packageLeaveAfter905 = [32, 25]
packageLeaveAfter905AndBefore1030 = [6, 28]
wrongAddressPackage = 9

# Load graph
g = Graph()
g = loadData.loadDistance("data/WGUPS Distance Table.csv")

# Load package to hash table
allPackages = ChainingHashTable()
loadData.loadPackages("data/WGUPS Package File.csv", allPackages)

station = " Salt Lake City, UT 84107"

# Truck's velocity (in second)
truckSpeed = 3600/18

# Predefine timestamps
tenThirty = datetime.timedelta(minutes=10*60+30)
tenTwenty = datetime.timedelta(minutes=10*60+20)
nineFive = datetime.timedelta(minutes=9*60+5)

# This function will return a intersection of two lists
def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

def findAllAdjacentEdges(currentPackage, packageSet):
    allAdjacentEdges = []

    if isinstance(currentPackage, str):
        for p in packageSet:
            allAdjacentEdges.append([p, g.connections[(currentPackage, allPackages.search(p).address)]])
    else:
        for p in packageSet:
            allAdjacentEdges.append([p, g.connections[(allPackages.search(currentPackage).address, allPackages.search(p).address)]])

    return sorted(allAdjacentEdges, key=lambda x: x[1])

def findOptimalPath(truck, startTime):
    truckHasWrongPackage = False
    if wrongAddressPackage in truck:
        truckHasWrongPackage = True
        truck.remove(9)
    optimalPath = {}
    packageBefore1030InTruck = intersection(truck, packageBefore1030)
    nearestVertex = findAllAdjacentEdges(station, truck)[0]
    package = nearestVertex[0]
    distance = nearestVertex[1]
    currentTime = startTime + datetime.timedelta(seconds=int(distance * truckSpeed))
    toAddress = allPackages.search(nearestVertex[0]).address
    truck.remove(package)

    if all(p in truck for p in packageBefore1030InTruck) and len(packageBefore1030InTruck) != 0:
        if packageBefore1030InTruck != 0:
            if package in packageBefore1030InTruck:
                packageBefore1030InTruck.remove(package)
            while True:
                after905 = False
                optimalPath[package] = [toAddress, distance, currentTime]
                nearestVertex = findAllAdjacentEdges(package, packageBefore1030InTruck)[0]
                if all(p in truck for p in packageLeaveAfter905AndBefore1030):
                    if currentTime > nineFive and len(packageLeaveAfter905AndBefore1030) != 0:
                        nearestVertex = findAllAdjacentEdges(package, packageLeaveAfter905AndBefore1030)[0]
                        packageLeaveAfter905AndBefore1030.remove(nearestVertex[0])
                        after905 = True
                package = nearestVertex[0]
                distance = nearestVertex[1]
                currentTime += datetime.timedelta(seconds=int(distance * truckSpeed))
                toAddress = allPackages.search(nearestVertex[0]).address
                if not after905:
                    packageBefore1030InTruck.remove(package)
                truck.remove(package)

                if len(packageBefore1030InTruck) == 0:
                    break

    while True:
        optimalPath[package] = [toAddress, distance, currentTime]
        nearestVertex = findAllAdjacentEdges(package, truck)[0]
        if truckHasWrongPackage:
            if currentTime > tenTwenty:
                allPackages.search(wrongAddressPackage).address = " 410 S State St"
                truck.append(wrongAddressPackage)
                truckHasWrongPackage = False
        if all(p in truck for p in packageLeaveAfter905AndBefore1030):
            if currentTime > nineFive and len(packageLeaveAfter905AndBefore1030) != 0:
                nearestVertex = findAllAdjacentEdges(package, packageLeaveAfter905AndBefore1030)[0]
                packageLeaveAfter905AndBefore1030.remove(nearestVertex[0])
        package = nearestVertex[0]
        distance = nearestVertex[1]
        currentTime += datetime.timedelta(seconds=int(distance * truckSpeed))
        toAddress = allPackages.search(nearestVertex[0]).address
        truck.remove(package)
        if len(truck) == 0:
            optimalPath[package] = [toAddress, distance, currentTime]
            break

    return optimalPath