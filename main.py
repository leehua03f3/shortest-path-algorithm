# Student Name: Duy Hua
# Student ID: 002885892

from loadData import Graph
import loadData
import datetime
from chainingHashTable import ChainingHashTable
import dijkstra

# Load package to hash table
allPackages = ChainingHashTable()
loadData.loadPackages("data/WGUPS Package File.csv", allPackages)

startTime = datetime.timedelta(hours=8)

truck_1 = []
truck_2 = []
truck_3 = []

# Condition for all the packages
packageBefore1030 = [1, 13, 14, 16, 20, 29, 30, 31, 34, 37, 40]
packageGoTogether = [13, 14, 15, 16, 19, 20]
packageGoToTruck2 = [3, 18, 36, 38]
packageLeaveAfter905 = [32, 28]
packageLeaveAfter905AndBefore1030 = [6, 25]
wrongAddressPackage = 9

# Load packages to the truck
truck_1 += packageBefore1030[0:int(len(packageBefore1030)/2)]
packageBefore1030Copy = packageBefore1030.copy()
for p in packageBefore1030[0:int(len(packageBefore1030)/2)]:
    packageBefore1030Copy.remove(p)
truck_2 += packageBefore1030Copy
truck_2 += packageLeaveAfter905AndBefore1030
truck_2 += packageGoToTruck2
truck_3 += packageLeaveAfter905
truck_3.append(wrongAddressPackage)

remainingPackages = list(range(1,41))
for p in truck_1 + truck_2 + truck_3:
    remainingPackages.remove(p)

for p in remainingPackages:
    if len(truck_1) != 16:
        truck_1.append(p)
        continue
    if len(truck_2) != 16:
        truck_2.append(p)
        continue
    truck_3.append(p)
# End load packages to trucks

# print(truck_1)
# print(truck_2)
# print(truck_3)

# Get delivery information from first and second truck
truck1OptimalPath = dijkstra.findOptimalPath(truck_1, startTime)
truck2OptimalPath = dijkstra.findOptimalPath(truck_2, startTime)

# Find out whether truck 1 or truck 2 finish the delivery first
truck1LastPackageTime = startTime
for k,v in truck1OptimalPath.items():
    if v[2] > truck1LastPackageTime:
        truck1LastPackageTime = v[2]

truck2LastPackageTime = startTime
for k,v in truck2OptimalPath.items():
    if v[2] > truck2LastPackageTime:
        truck2LastPackageTime = v[2]

# Get the lastest delivery time of the truck which finishes delivery first
if truck1LastPackageTime > truck2LastPackageTime:
    truck3StartTime = truck2LastPackageTime
else:
    truck3StartTime = truck1LastPackageTime

# The driver from the finished truck go to the third truck
startTime = truck3StartTime
truck3OptimalPath = dijkstra.findOptimalPath(truck_3, startTime)

totalDistance = 0

for k, v in truck1OptimalPath.items():
    totalDistance += v[1]
    allPackages.search(k).setDeliveryTime(v[2])
    # print(k, v[0], v[2])

for k, v in truck2OptimalPath.items():
    totalDistance += v[1]
    allPackages.search(k).setDeliveryTime(v[2])
    # print(k, v[0], v[2])

for k, v in truck3OptimalPath.items():
    totalDistance += v[1]
    allPackages.search(k).setDeliveryTime(v[2])
    # print(k, v[0], v[2])

# Ask user to input a specific time
while True:
    try:
        startTime = input("Enter start time (HH:MM:SS): ")
        startTime = startTime.split(":")
        startHour = int(startTime[0])
        startMinute = int(startTime[1])
        startSecond = int(startTime[2])

        # Validate user input
        if (startSecond > 60 or startSecond < 0) or (startMinute > 60 or startMinute < 0) or (
                startHour > 24 or startHour < 0):
            print("Invalid time, please try again")
            continue

        endTime = input("Enter end time (HH:MM:SS): ")
        endTime = endTime.split(":")
        endHour = int(endTime[0])
        endMinute = int(endTime[1])
        endSecond = int(endTime[2])

        if (endSecond > 60 or endSecond < 0) or (endMinute > 60 or endMinute < 0) or (endHour > 24 or endHour < 0):
            print("Invalid time, please try again")
            continue

        # Convert user input to datetime object
        startTime = datetime.timedelta(seconds=(startSecond + startMinute * 60 + startHour * 3600))
        endTime = datetime.timedelta(seconds=(endSecond + endMinute * 60 + endHour * 3600))

        if startTime > endTime:
            print("Start Time and not be after End Time")
            continue

        break
    except Exception:
        print("Please enter the format 'HH:MM:SS'")

# Merge all delivery info from all trucks
allDeliveryInfo = truck1OptimalPath|truck2OptimalPath|truck3OptimalPath

print("----------------")

# Print report
for p in range(1,41):
    if allDeliveryInfo[p][2] >= startTime and allDeliveryInfo[p][2] > endTime:
        allPackages.search(p).setStatus("at the hub")
    elif allDeliveryInfo[p][2] < endTime and allDeliveryInfo[p][2] < startTime:
        allPackages.search(p).setStatus("delivered")
    else:
        allPackages.search(p).setStatus("en route")
    if allPackages.search(p).status == 'delivered':
        print("Package " + str(p) + " - " + "Status: " + allPackages.search(p).status + " at " + str(allPackages.search(p).deliveryTime))
    else:
        print("Package " + str(p) + " - " + "Status: " + allPackages.search(p).status)

print("----------------")

print("Total Distance: " + str(totalDistance))