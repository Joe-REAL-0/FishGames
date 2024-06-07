from .DatabaseManager import Database
from .FishDataManager import FishDataManager

def checkFishMain(fishName):
    db=Database()
    userId,nickname=db.selectFishOwner(fishName)
    fishValue = FishDataManager().getFishByName(fishName)[2]
    db.close()

    if userId == None:
        return f"鱼塘里没有这种鱼！"
    else:
        return f"这条鱼由{nickname}({userId})放生！\n价值:{fishValue} points/条"
    
