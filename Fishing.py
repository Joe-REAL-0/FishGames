from .DatabaseManager import Database
from random import random
from functools import reduce
from datetime import datetime,timedelta

fishingCoolDownDict = {}

def findFishInPool(weight, poolData):
    totalCount = reduce(lambda acc, x: acc + x[1], poolData, 0)
    cycleCount = 0
    for fish in poolData:
        cycleCount += fish[2]
        if weight < cycleCount/totalCount:
            return fish

def fishingMain(id):
    db=Database(id)
    poolData=db.selectPool()
    if len(poolData) == 0: return "池塘里暂时没有鱼,请晚点再来"
    if id in fishingCoolDownDict and fishingCoolDownDict[id] > datetime.now():
        time_difference = fishingCoolDownDict[id] - datetime.now()
        time_in_seconds = time_difference.total_seconds()
        time_string = f"{int(time_in_seconds/3600)}小时 {int(time_in_seconds%3600/60)}分钟"
        return f"每2小时可以钓鱼一次!\n你距离下次可钓鱼剩余:\n  {time_string}  "
    else:
        fishingCoolDownDict[id] = datetime.now() + timedelta(hours=2)
    level=db.selectLevel()
    successRate=0.4 if level > 9 else 0.8-(level-1)*0.04
    fishDic = {}
    totalValue = 0
    message = f"使用 Lv.{level} 的魚竿釣魚\n抛竿 {level} 次\n-----------\n"
    for i in range(level):
        if random() > successRate: 
            continue
        fish = findFishInPool(random(), poolData)
        fishDic[fish[0]] = fishDic.get(fish[0], 0) + 1
        totalValue += fish[1]
        db.reduceFish(fish[0])
        fish[2] -= 1 if fish[2] > 1 else poolData.remove(fish)
        if (len(poolData) == 0): break
    if len(fishDic) == 0:
        message += "运气不佳，一条鱼都没钓到"
    else:
        message += "你钓到了:\n"
        for fishName in fishDic:
            message += f"{fishName} *{fishDic[fishName]}\n"
        message += f"出售这些鱼获得了: {totalValue} points"
        db.changePoint(totalValue)
    db.close()
    return message