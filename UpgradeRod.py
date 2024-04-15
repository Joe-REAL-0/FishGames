from .DatabaseManager import Database
from math import exp

def upgradeMain(id):
    db = Database(id)
    level = db.selectLevel()
    point = db.selectPoint()
    pointNeeded = int(exp(level-1)*20)
    if point < pointNeeded:
        message = f"升级鱼竿到Lv. {level+1} \n需要 {pointNeeded} points\n你的信用点不足"
    else:
        message = f"你的鱼竿成功升级\nLv.{level} -> Lv. {level + 1}\n消耗 {pointNeeded} points\n信用点余额 {point - pointNeeded} points"
        db.increaseLevel()
    db.close()
    return message
