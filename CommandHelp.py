def helpMain(command:str = None):
    if(command == None):
        message = "[钓鱼游戏]是一款由Joe开发的开放世界冒险游戏，在游戏中，玩家将扮演名为[赛博钓鱼佬]的神秘角色，成为天选之子，掌握[放生]之力，并在每隔两小时一次的钓鱼过程中邂逅形态多样能力各异的[鱼]们，在激动人心的钓鱼过程中，逐步探索并发掘[鱼塘]背后的真相\n"
        message+= "----------\n"
        message+= "钓鱼游戏指令：\n"
        message+= "[钓鱼] - 开始钓鱼\n"
        message+= "[放生 鱼名] - 向鱼塘中放生鱼\n"
        message+= "[出售 编号 数量] - 卖出背包中某个编号的鱼\n"
        message+= "[排行榜] - 查看全服玩家的总资产排名\n"
        message+= "[升级鱼竿] - 升级钓鱼等级\n"
        message+= "[升级背包] - 升级背包容量\n"
        message+= "[查询鱼 鱼名] - 查询鱼的信息\n"
        message+= "[我的信息] - 查询个人信息\n"
        message+= "[鱼塘大屏] - 查看鱼塘信息"
        return message