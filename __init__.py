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
from .ListFish import listFishMain
from .CheckFish import checkFishMain
from .CheckUser import checkUserMain

helpCommand = on_command('钓鱼游戏')
release = on_command('放生')
fishing = on_command('钓鱼')
sellFish = on_command('出售')
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
    

@release.handle()
async def release_handle(bot:Bot, event: Event, args:Message = CommandArg()):
    user_id = event.get_user_id()
    check_account(event)
    args_sp = args_sp = args.extract_plain_text().split(" ")
    fishName = args_sp[0]
    c=MessageSegment.reply(event.message_id)
    message = releaseMain(user_id, fishName)
    await release.finish(c+Message(message))

@fishing.handle()
async def fishing_handle(bot:Bot, event: Event):
    check_account(event)
    user_id = event.get_user_id()
    message = fishingMain(user_id)
    c=MessageSegment.reply(event.message_id)
    await fishing.finish(c+Message(message))

@sellFish.handle()
async def sellFish_handle(bot:Bot, event: Event, args:Message = CommandArg()):
    check_account(event)
    user_id = event.get_user_id()
    fishName = args.extract_plain_text()
    message = SellFishMain(user_id, fishName)
    c=MessageSegment.reply(event.message_id)
    await sellFish.finish(c+Message(message))

@upgradeRod.handle()
async def upgrade_handle(bot:Bot, event: Event):
    check_account(event)
    user_id = event.get_user_id()
    message = upgradeRodMain(user_id)
    c=MessageSegment.reply(event.message_id)
    await upgradeRod.finish(c+Message(message))

@upgradeBackpack.handle()
async def upgrade_handle(bot:Bot, event: Event):
    check_account(event)
    user_id = event.get_user_id()
    message = upgradeBackpackMain(user_id)
    c=MessageSegment.reply(event.message_id)
    await upgradeBackpack.finish(c+Message(message))

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
    check_account(event)
    message = leaderboardMain()
    c=MessageSegment.reply(event.message_id)
    await leaderboard.finish(c+Message(message))

@checkFish.handle()
async def checkFish_handle(bot:Bot, event: Event, args:Message = CommandArg()):
    check_account(event)
    fishName = args.extract_plain_text()
    message = checkFishMain(fishName)
    c=MessageSegment.reply(event.message_id)
    await checkFish.finish(c+Message(message))

@checkUser.handle()
async def checkUser_handle(bot:Bot, event: Event):
    check_account(event)
    user_id = event.get_user_id()
    message = checkUserMain(user_id)
    c=MessageSegment.reply(event.message_id)
    await checkUser.finish(c+Message(message))

@helpCommand.handle()
async def helpCommand_handle(bot:Bot, event: Event):
    check_account(event)
    message = helpMain()
    c=MessageSegment.reply(event.message_id)
    await helpCommand.finish(c+Message(message))

