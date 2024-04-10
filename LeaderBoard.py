from .DatabaseManager import Database
from itertools import product

def calculateRodValue(level):
    return sum(int(20 * (2 ** (i - 1))) for i in range(1, level + 1))

def leaderboardMain():
    db = Database()
    allUserList = db.selectAllUser()
    allRodLevelList = db.selectAllLevel()
    matchingUserList = list(filter(lambda x: x[0][0] == x[1][0] in product(allUserList, allRodLevelList)))
    allUserWealthList = list(map(lambda x: (x[0][0], x[0][1], x[0][2] + calculateRodValue(x[1][1])), matchingUserList))
    allUserWealthList.sort(key=lambda x: x[2])
    message = "排行榜\n----------\n"
    if len(allUserWealthList) > 5:
        allUserWealthList = allUserWealthList[:5]
        message += "*当前显示排行榜前5名\n"
    for i, user in enumerate(allUserWealthList):
        message += f"{i + 1}. {user[1]}({user[0]}) - {user[2]} points\n"
    db.close()
    return message