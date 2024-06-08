from PlayerBackPack import BackPack

def SellAllFishMain(id):
    backpack = BackPack(id)
    if (backpack.isEmpty()):
        return "背包里没有鱼！使用指令[钓鱼]从鱼塘中获取一些鱼吧！"
    totalValue = backpack.getTotalValue()
    backpack.sell_all_fish()
    return f"成功出售所有鱼！\n出售这些鱼获得了 {totalValue} points！"