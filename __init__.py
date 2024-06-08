from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message, Bot, Event ,MessageSegment
import aiofiles.os
from .DatabaseManager import Database
from .CommandHelp import helpMain
from .Fishing import fishingMain
from .ReleaseFish import releaseMain
from .UpgradeRod import upgradeRodMain
from .UpgradeBackpack import upgradeBackpackMain
from .LeaderBoard import leaderboardMain
from .SellFish import SellFishMain
from .SellAllFish import SellAllFishMain
from .ListFish import listFishMain
from .CheckFish import checkFishMain
from .CheckUser import checkUserMain
import traceback

helpCommand = on_command('钓鱼游戏')
release = on_command('放生')
fishing = on_command('钓鱼')
sellFish = on_command('出售')
sellAllFish = on_command('一键出售')
upgradeRod = on_command('升级鱼竿')
upgradeBackpack = on_command('升级背包')
listPool = on_command('鱼塘大屏')
leaderboard = on_command('排行榜')
checkFish = on_command('查询鱼')
checkUser = on_command('我的信息')

def check_account(event):
    user_id = event.get_user_id()
    nickname = event.sender.nickname
    db = Database(user_id)
    db.checkAccount(nickname)
    db.close()

@helpCommand.handle()
async def helpCommand_handle():
    await helpCommand.send(helpMain())

@release.handle()
async def release_handle(bot:Bot, event: Event, args:Message = CommandArg()):
    try:
        user_id = event.get_user_id()
        check_account(event)
        args_sp = args.extract_plain_text().split(" ")
        fishName = args_sp[0]
        c=MessageSegment.reply(event.message_id)
        message =c + Message(releaseMain(user_id, fishName))
    except:
        message=traceback.format_exc()
    await release.finish(message)

@fishing.handle()
async def fishing_handle(bot:Bot, event: Event):
    try:
        check_account(event)
        user_id = event.get_user_id()
        c=MessageSegment.reply(event.message_id)
        message =c+ Message(fishingMain(user_id))
    except:
        message=traceback.format_exc()
    await fishing.finish(message)

@sellFish.handle()
async def sellFish_handle(bot:Bot, event: Event, args:Message = CommandArg()):
    try:
        check_account(event)
        user_id = event.get_user_id()
        asp = args.extract_plain_text().split(" ")
        if(len(asp)!=2):
            message= SellFishMain(user_id)
        else:
            index = int(asp[0])
            amount = int(asp[1])
            message = SellFishMain(user_id, index , amount)
        message=MessageSegment.reply(event.message_id)+message
    except:
        message=traceback.format_exc()
    await sellFish.finish(message)

@sellAllFish.handle()
async def sellAllFish_handle(bot:Bot, event: Event):
    try:
        check_account(event)
        user_id = event.get_user_id()
        message = SellAllFishMain(user_id)
        message=MessageSegment.reply(event.message_id)+message
    except:
        message=traceback.format_exc()
    await sellAllFish.finish(message)

@upgradeRod.handle()
async def upgrade_handle(bot:Bot, event: Event):
    try:
        check_account(event)
        user_id = event.get_user_id()
        message = upgradeRodMain(user_id)
        message=MessageSegment.reply(event.message_id)+message
    except:
        message=traceback.format_exc()
    await upgradeRod.finish(message)

@upgradeBackpack.handle()
async def upgrade_handle(bot:Bot, event: Event):
    try:
        check_account(event)
        user_id = event.get_user_id()
        message = upgradeBackpackMain(user_id)
        message=MessageSegment.reply(event.message_id)+message
    except:
        message=traceback.format_exc()
    await upgradeBackpack.finish(message)

@listPool.handle()
async def listPool_handle(bot:Bot, event: Event):
    check_account(event)
    msg=listFishMain()
    c=MessageSegment.reply(event.message_id)
    if msg[0]=='/':
        await listPool.send(c+MessageSegment.image(msg))
        await aiofiles.os.remove(msg)
    else:
        await listPool.finish(c+Message(msg))
    

@leaderboard.handle()
async def leaderboard_handle(bot:Bot, event: Event):
    try:
        check_account(event)
        message = leaderboardMain()
        message=MessageSegment.reply(event.message_id)+message
    except:
        message=traceback.format_exc()
    await leaderboard.finish(message)

@checkFish.handle()
async def checkFish_handle(bot:Bot, event: Event, args:Message = CommandArg()):
    try:
        check_account(event)
        fishName = args.extract_plain_text()
        message = checkFishMain(fishName)
        message=MessageSegment.reply(event.message_id)+message
    except:
        message=traceback.format_exc()
    await checkFish.finish(message)

@checkUser.handle()
async def checkUser_handle(bot:Bot, event: Event):
    try:
        check_account(event)
        user_id = event.get_user_id()
        message = checkUserMain(user_id)
        message=MessageSegment.reply(event.message_id)+message
    except:
        message=traceback.format_exc()
    await checkUser.finish(message)

