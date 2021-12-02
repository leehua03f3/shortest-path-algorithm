from chainingHashTable import ChainingHashTable
import loadData
import time

startTime = time.time()

hashTable = ChainingHashTable()
loadData.loadPackages("data/testFile.csv", hashTable)

print("--- %s seconds ---" % (time.time() - startTime))