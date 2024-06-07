from .DatabaseManager import Database
from PlayerBackPack import BackPack

def checkUserMain(user_id):
    db = Database(user_id)
    userInfo = db.selectUser()
    rodLevel = db.selectRodLevel()
    backpackLevel = db.selectBackpackLevel()
    db.close()

    message = f"用户ID: {user_id}\n"
    message += f"昵称: {userInfo[0][1]}\n"
    message += f"信用点余额: {userInfo[0][2]} points\n"
    message += "----------\n"
    message += f"鱼竿等级: Lv.{rodLevel}\n"
    message += f"背包等级: Lv.{backpackLevel}\n"
    BackPack(user_id).listBackpackFish
    return message