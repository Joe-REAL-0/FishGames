from datetime import datetime
from .DatabaseManager import Database
import numpy as np
import math

time = datetime.now()

def generateFishPrice(originPrice):
    z = np.random.normal(0, 0.8) * 0.1
    prize = int(math.ceil(originPrice * (1 + z))) if (originPrice * (1 + z)) > 10 else 10
    return prize

class FishDataManager:
    _instance = None
    def __init__(self):
        self.fishData = [list(i) for i in Database().selectPool()]
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(FishDataManager, cls).__new__(cls)
        return cls._instance
    
    def isEmpty(self):
        return len(self.fishData) == 0
    
    async def updateFishPrice(self):
        for fish in self.fishData:
            fishValue = fish[1]
            fish[1] = generateFishPrice(fishValue)
        Database().updatePool(self.fishData)

    def getFishRandomly(self):
        totalWeight = sum([fish[2] for fish in self.fishData])
        if totalWeight == 0: return None
        weights = [(fish[2]/totalWeight) for fish in self.fishData]
        index = np.random.choice(range(len(self.fishData)), p=weights)
        return self.fishData[index]
    
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
    
    def addFish(self, *args):
        if len(args) == 1 and isinstance(args[0], list):
            self.fishData.append(args[0])
        elif len(args) == 3:
            ownerID, fishName, fishValue = args
            self.fishData.append([fishName, fishValue, 50, ownerID])
        else:
            raise ValueError("Invalid arguments")
    
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
                if fish[2] == 0: self.fishData.remove(fish)
                break

    def increaseFish(self, fish, amount):
        for f in self.fishData:
            if f[0] == fish[0]:
                f[2] += amount
                return
        self.addFish(fish)