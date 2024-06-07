from .FishDataManager import FishDataManager
from .PlayerBackPack import BackPack

def SellFishMain(id, index, amount):
    backpack = BackPack(id)
    if (backpack.isEmpty()):
        return "背包里没有鱼！使用指令[钓鱼]从鱼塘中获取一些鱼吧！"
    if (backpack.sell_fish(index - 1, amount)):
        return f"成功出售{amount}条鱼！"
    else:
        return "出售失败！请检查编号和数量！\n" + backpack.listBackpackFish()
    