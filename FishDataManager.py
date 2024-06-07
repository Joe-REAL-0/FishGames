from datetime import datetime
from .DatabaseManager import Database
import numpy as np
import math

time = datetime.now()

def generateFishPrice(originPrice):
    z = np.random.normal(0, 0.8) * 0.1
    return int(math.ceil(originPrice * (1 + z)))

class FishDataManager:
    _instance = None
    def __init__(self):
        self.fishData = [list(i) for i in Database().selectPool()]
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(FishDataManager, cls).__new__(cls)
        return cls._instance
    
    async def updateFishPrice(self):
        for fish in self.fishData:
            fishValue = fish[1]
            fish[1] = generateFishPrice(fishValue)
        Database().updatePool(self.fishData)

    def getFishRandomly(self):
        return self.fishData[np.random.randint(0, len(self.fishData))]
    
    def getFishByName(self, fishName):
        for fish in self.fishData:
            if fish[0] == fishName:
                return fish
        return None
    
    def getFishIndex(self, fishName):
        for i in range(len(self.fishData)):
            if self.fishData[i][0] == fishName:
                return i
        return None
    
    def addFish(self, ownerID, fishName, fishValue):
        self.fishData.append([fishName, fishValue, 50, ownerID])
        Database(ownerID).insertFish(fishName, fishValue)

    def removeFish(self, fishName):
        for fish in self.fishData:
            if fish[0] == fishName:
                self.fishData.remove(fish)
                break
        Database().removeFish(fishName)

    def reduceFish(self, fishName):
        for fish in self.fishData: 
            if fish[0] == fishName:
                fish[2] -= 1
                if fish[2] == 0:
                    self.fishData.remove(fish)
                break
        Database().reduceFish(fishName)