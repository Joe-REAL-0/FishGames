from .FishDataManager import FishDataManager
from .PlayerBackPack import BackPack

def SellFishMain(id, index = None, amount = None):
    backpack = BackPack(id)
    if (index == None or amount == None):
        return "请使用指令[出售 编号 数量]来出售鱼！\n" + backpack.listBackpackFish()
    if (backpack.isEmpty()):
        return "背包里没有鱼！使用指令[钓鱼]从鱼塘中获取一些鱼吧！"
    fish = backpack.get_fish(index - 1)
    totalValue = fish[2] * amount
    if (backpack.sell_fish(index - 1, amount)):
        return f"成功出售{amount}条{fish[0]}！\n出售这些鱼获得了 {totalValue} points！"
    else:
        return "出售失败！请检查编号和数量！\n" + backpack.listBackpackFish()