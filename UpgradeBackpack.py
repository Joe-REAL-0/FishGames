from .DatabaseManager import Database
from .PlayerBackPack import BackPack

def upgradeBackpackMain(id):
    db = Database(id)
    level = db.selectRodLevel()
    point = db.selectPoint()
    pointNeeded = int((2.5**level) * 15)
    if point < pointNeeded:
        message = f"升级鱼竿到Lv. {level+1} \n需要 {pointNeeded} points\n你的信用点不足"
    else:
        message = f"你的背包成功升级\n Lv.{level} -> Lv. {level + 1}"
        message += f"\n背包容量增加至 {(level + 1) * 3 +1}"
        BackPack(id).capacity = (level + 1) * 3 + 1
        message += f"\n消耗 {pointNeeded} points"
        message += f"\n信用点余额 {point - pointNeeded} points"
        db.increaseBackpackLevel()
    db.close()
    return message