from .DatabaseManager import Database
from .FishDataManager import FishDataManager
from .PlayerBackPack import BackPack
from random import random
from asyncio import create_task
from datetime import datetime,timedelta

fishingCoolDownDict = {}

def fishingMain(user_id):
    fishManager = FishDataManager()
    backpack = BackPack(user_id)
    db = Database(user_id)
    if fishManager.isEmpty(): return "池塘里暂时没有鱼,请晚点再来"
    if user_id in fishingCoolDownDict and fishingCoolDownDict[user_id] > datetime.now():
        time_difference = fishingCoolDownDict[user_id] - datetime.now()
        time_in_seconds = time_difference.total_seconds()
        time_string = f"{int(time_in_seconds/3600)}小时 {int(time_in_seconds%3600/60)}分钟"
        return f"每2小时可以钓鱼一次!\n你距离下次可钓鱼剩余:\n  {time_string}  "
    else:
        fishingCoolDownDict[user_id] = datetime.now() + timedelta(hours=2)
    level=db.selectRodLevel()
    successRate=0.4 if level > 9 else 0.8-(level-1)*0.04
    fishDic = {}
    fishingTimes = level if level <= 5 else level + 2*(level-5)
    message = f"使用 Lv.{level} 的鱼竿\n抛竿 {fishingTimes} 次\n-----------\n"
    for i in range(fishingTimes):
        if random() > successRate: continue
        fish = fishManager.getFishIndexRandomly()
        fishDic[fish] = fishDic.get(fish, 0) + 1
        fishManager.reduceFish(fish[0])
        if fishManager.isEmpty(): break
    if len(fishDic) == 0:
        message += "运气不佳，一条鱼都没钓到"
    else:
        message += "你钓到了:\n"
        for fish in fishDic:
            message += f"{fish[0]} *{fishDic[fish]}\n"
            if backpack.isFull():
                fishManager.addFish(fish)
            result = backpack.add_fish(fish, fishDic[fish])
            if not result: 
                message += "背包已满，有一些鱼逃回到鱼塘中了!"
                break
        message += "-----------\n"
        if not backpack.isFull():
            message += "这些鱼已经全部加入你的背包"
        db.updateBackpack(backpack.fishs)
        create_task(fishManager.updateFishPrice())

    return message