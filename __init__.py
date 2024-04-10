from nonebot.params import on_command, CommandArg
from nonebot.adapters.onebot.v11 import Message, Bot, Event
from .DatabaseManager import Database
from .CommandHelp import helpMain
from .Fishing import fishingMain
from .ReleaseFish import releaseMain
from .UpgradeRod import upgradeMain
from .ListFish import listFishMain
from .CheckFish import checkFishMain
from .CheckUser import checkUserMain

help = on_command('钓鱼游戏')
release = on_command('放生')
fishing = on_command('钓鱼')
upgrade = on_command('升级鱼竿')
listPool = on_command('鱼塘大屏')
dashboard = on_command('排行榜')
checkFish = on_command('查询鱼')
checkUser = on_command('信息查询')

def check_account(event):
    user_id = event.sender.user_id
    nickname = event.sender.nickname
    db = Database(user_id)
    db.checkAccount(nickname)
    db.close()
    

@release.handle()
async def release_handle(bot:Bot, event: Event, args:Message = CommandArg()):
    user_id = event.sender.user_id
    fishName = args.extract_plain_text()
    count = args.extract_plain_text()
    message = releaseMain(user_id, fishName, count)
    await release.finish(message)

@fishing.handle()
async def fishing_handle(bot:Bot, event: Event):
    user_id = event.sender.user_id
    message = fishingMain(user_id)
    await fishing.finish(message)

@upgrade.handle()
async def upgrade_handle(bot:Bot, event: Event):
    user_id = event.sender.user_id
    message = upgradeMain(user_id)
    await upgrade.finish(message)

@listPool.handle()
async def listPool_handle(bot:Bot, event: Event):
    db = Database()
    message = listFishMain()
    db.close()
    await listPool.finish(message)

@dashboard.handle()
async def dashboard_handle(bot:Bot, event: Event):
    db = Database()
    message = db.selectDashboard()
    db.close()
    await dashboard.finish(message)

@checkFish.handle()
async def checkFish_handle(bot:Bot, event: Event, args:Message = CommandArg()):
    fishName = args.extract_plain_text()
    message = checkFishMain(fishName)
    await checkFish.finish(message)

@checkUser.handle()
async def checkUser_handle(bot:Bot, event: Event):
    user_id = event.sender.user_id
    message = checkUserMain(user_id)
    await checkUser.finish(message)

@help.handle()
async def help_handle(bot:Bot, event: Event):
    message = helpMain()
    await help.finish(message)
    
    
    