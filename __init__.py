from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message, Bot, Event
from .DatabaseManager import Database
from .CommandHelp import helpMain
from .Fishing import fishingMain
from .ReleaseFish import releaseMain
from .UpgradeRod import upgradeMain
from .LeaderBoard import leaderboardMain
from .ListFish import listFishMain
from .CheckFish import checkFishMain
from .CheckUser import checkUserMain

help = on_command('钓鱼游戏')
release = on_command('放生')
fishing = on_command('钓鱼')
upgrade = on_command('升级鱼竿')
listPool = on_command('鱼塘大屏')
leaderboard = on_command('排行榜')
checkFish = on_command('查询鱼')
checkUser = on_command('信息查询')

def check_account(event):
    user_id = event.get_user_id()
    nickname = event.sender.nickname
    db = Database(user_id)
    db.checkAccount(nickname)
    db.close()
    

@release.handle()
async def release_handle(bot:Bot, event: Event, args:Message = CommandArg()):
    user_id = event.get_user_id()
    check_account(event)
    args_sp = args_sp = args.extract_plain_text().split(" ")
    fishName = args_sp[0]
    try:
        count = int(args_sp[1])
    except:
        await release.finish("放生失败！\n*鱼的数量必须是个数字!")
    message = releaseMain(user_id, fishName, count)
    await release.finish(message)

@fishing.handle()
async def fishing_handle(bot:Bot, event: Event):
    check_account(event)
    user_id = event.get_user_id()
    message = fishingMain(user_id)
    await fishing.finish(message)

@upgrade.handle()
async def upgrade_handle(bot:Bot, event: Event):
    check_account(event)
    user_id = event.get_user_id()
    message = upgradeMain(user_id)
    await upgrade.finish(message)

@listPool.handle()
async def listPool_handle(bot:Bot, event: Event):
    check_account(event)
    message = listFishMain()
    await listPool.finish(message)

@leaderboard.handle()
async def leaderboard_handle(bot:Bot, event: Event):
    check_account(event)
    message = leaderboardMain()
    await leaderboard.finish(message)

@checkFish.handle()
async def checkFish_handle(bot:Bot, event: Event, args:Message = CommandArg()):
    check_account(event)
    fishName = args.extract_plain_text()
    message = checkFishMain(fishName)
    await checkFish.finish(message)

@checkUser.handle()
async def checkUser_handle(bot:Bot, event: Event):
    check_account(event)
    user_id = event.get_user_id()
    message = checkUserMain(user_id)
    await checkUser.finish(message)

@help.handle()
async def help_handle(bot:Bot, event: Event):
    check_account(event)
    message = helpMain()
    await help.finish(message)   