from random import randint
from .DatabaseManager import Database
from datetime import datetime,timedelta

fishReleaseCoolDownDict = {}

def releaseMain(id,fishName,count):
    if not 3<=count<=30:
        return "放生失败！\n*鱼的数量必须在3-30之间"
    if not 0<len(fishName)<15:
        return "放生失败！\n*鱼的名称必须少于15字"
    db = Database(id)
    if len(db.selectFish(fishName)) != 0:
        db.close()
        return "放生失败！\n*鱼塘里已经存在这种鱼了！不能重复放生！"
    if id in fishReleaseCoolDownDict and fishReleaseCoolDownDict[id] > datetime.now():
        time_difference = fishReleaseCoolDownDict[id] - datetime.now()
        time_in_seconds = time_difference.total_seconds()
        time_string = f"{int(time_in_seconds/3600)}小时 {int(time_in_seconds%3600/60)}分钟" if time_in_seconds > 60 else f"{int(time_in_seconds)}秒"
        return f"放生失败！\n*每6小时只能放生一次!\n你距离下次放生还有:{time_string}"
    else:
        fishReleaseCoolDownDict[id] = datetime.now() + timedelta(hours=6)
    k=randint(0,3)
    value = randint((65-count*2)-k, (68-count*2)-k)
    db.insertFish(fishName, value, count)
    db.close()
    return f"放生成功！鱼塘因为 {fishName} 的加入变得更热闹了！\n目前这种鱼价值 {value} points/条"