from .DatabaseManager import Database

def checkUserMain(user_id):
    db = Database(user_id)
    userInfo = db.selectUserInfo()
    db.close()
    message = f"用户ID: {user_id}\n"
    message += f"昵称: {userInfo[0]}\n"
    message += f"信用点余额: {userInfo[1]} points\n"
    return message