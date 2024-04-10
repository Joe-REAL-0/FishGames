from .DatabaseManager import Database

def checkFishMain(fishName):
    db=Database()
    userId,nickname=db.selectFishOwner(fishName)
    db.close()
    if userId==None:
        return f"鱼塘里没有这种鱼！"
    else:
        return f"这种鱼由{nickname}({userId})放生！"