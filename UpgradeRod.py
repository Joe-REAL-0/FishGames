from .DatabaseManager import Database
from math import exp

def upgradeRodMain(id):
    db = Database(id)
    level = db.selectRodLevel()
    point = db.selectPoint()
    pointNeeded = int(exp(level-1)*20)
    fishingTimes = (level +1) if ((level +1) <= 5) else ((level +1) + 2*((level +1)-5))
    if point < pointNeeded:
        message = f"升级鱼竿到Lv. {level+1} \n需要 {pointNeeded} points\n你的信用点不足"
    else:
        message = f"你的鱼竿成功升级\n Lv.{level} -> Lv. {level + 1}"
        message += f"\n每次钓鱼的抛竿次数升级到 {fishingTimes} "
        message += f"\n消耗 {pointNeeded} points "
        message += f"\n信用点余额 {point - pointNeeded} points"
        db.increaseRodLevel()
    db.close()
    return message
