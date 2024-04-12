from .DatabaseManager import Database
from itertools import product
from math import exp

def calculateRodValue(level):
    return sum(int(20 * (exp(i - 1))) for i in range(1, level))

def leaderboardMain():
    db = Database()
    allUserList = db.selectAllUser()
    allRodLevelList = db.selectAllLevel()
    matchingUserList = list(filter(lambda x: x[0][0] == x[1][0] , product(allUserList, allRodLevelList)))
    allUserWealthList = list(map(lambda x: (x[0][0], x[0][1], x[0][2] ,calculateRodValue(x[1][1])), matchingUserList))
    allUserWealthList.sort(key=lambda x: x[2]+x[3], reverse=True)
    message = "排行榜\n----------\n"
    if len(allUserWealthList) > 5:
        allUserWealthList = allUserWealthList[:5]
        message += "*当前显示排行榜前5名\n"
    for i, user in enumerate(allUserWealthList):
        message += f"{i + 1}. {user[1]}({user[0]})\n 总资产:{user[2]+user[3]} points\n鱼竿价值:{user[3]} points\n"
    db.close()
    return message