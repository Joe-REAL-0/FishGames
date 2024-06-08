from .DatabaseManager import Database

class BackPack:
    def __init__(self, user_id):
        self.user_id = user_id
        self.fishs = Database(user_id).selectBackpack()
        level = Database(user_id).selectBackpackLevel()
        self.capacity = level * 3 + 1

    def getTotalValue(self):
        totalValue = 0
        for fish in self.fishs:
            totalValue += fish[1] * fish[2]
        return totalValue
    
    def get_fish(self, fish):
        if type(fish) == int:
            return self.fishs[fish]
        elif type(fish) == str:
            for f in self.fishs:
                if fish == f[0]:
                    return f
        elif type(fish) == list:
            return self.fishs.index(fish)

    def add_fish(self, fish, amount):
        if self.isFull():
            return False
        for f in self.fishs:
            if fish[0] == f[0]:
                fish[1] += amount
                return True
        self.fishs.append([fish[0], amount, fish[2], self.user_id])
        return True

    def remove_fish(self, fish):
        if not fish in self.fishs: return False
        self.fishs.remove(fish)
        return True
    
    def sell_fish(self, index, amount):
        if index >= len(self.fishs): return False
        fish = self.fishs[index]
        db = Database(self.user_id)
        if fish[1] < amount: return False
        if fish[1] == amount:
            self.fishs.remove(fish)
        else:
            fish[1] -= amount
        db.changePoint(fish[2] * amount)
        db.updateBackpack(self.fishs)
        db.close()
        return True
    
    def sell_all_fish(self):
        db = Database(self.user_id)
        totalValue = self.getTotalValue()
        db.changePoint(totalValue)
        self.fishs = []
        db.updateBackpack(self.fishs)
        db.close()

    def isEmpty(self):
        return len(self.fishs) == 0
    
    def isFull(self):
        totalFish = 0
        for fish in self.fishs:
            totalFish += fish[1]
        return totalFish == self.capacity

    def listBackpackFish(self):
        if self.isEmpty(): return "背包数据: 空\n"
        message = "----------\n背包数据:\n"
        for i,fish in enumerate(self.fishs):
            message += f"{i+1} {fish[0]} *{fish[1]}\n   - (价值 {fish[2]}/条)\n"
        message += f"----------\n"
        message += f"背包容量: {len(self.fishs)}/{self.capacity}\n"
        message += "使用指令[出售 编号 数量]可以出售背包中的鱼\n"
        return message
