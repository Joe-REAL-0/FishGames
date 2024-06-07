from .DatabaseManager import Database

class BackPack:
    def __init__(self, user_id):
        self.user_id = user_id
        self.fishs = Database(user_id).selectBackpack()
        level = Database(user_id).selectBackpackLevel()
        self.capacity = level * 3 + 1

    def get_fish(self, index):
        return self.fishs[index]
    
    def get_fish(self, fish):
        return self.fishs.index(fish)

    def add_fish(self, fish):
        if self.isFull():
            return False
        if fish in self.fishs:
            self.get_fish(fish)[1] += 1
            return True
        self.fishs[self.user_id] = [fish[0], 1, fish[1], self.user_id]
        return True

    def remove_fish(self, fish):
        if not fish in self.fishs: return False
        self.fishs.remove(fish)
        return True
    
    def sell_fish(self, index, amount):
        fish = self.get_fish(index)
        if fish[1] < amount: return False
        if fish[1] == amount:
            self.fishs.remove(fish)
        else:
            fish[1] -= amount
        Database(self.user_id).changePoint(fish[2] * amount)
        return True

    def isEmpty(self):
        return len(self.fishs) == 0
    
    def isFull(self):
        return len(self.fishs) == self.capacity
    
    def updateBackpack(self):
        Database(self.user_id).updateBackpack(self.fishs)

    def listBackpackFish(self):
        message = "----------\n背包数据:"
        for i,fish in enumerate(self.fishs):
            message += f"{i+1} {fish[0]} *{fish[1]}\n   - (价值 {fish[2]}/条)\n"
        message += f"----------\n"
        message += f"背包容量: {len(self.fishs)}/{self.capacity}\n"
        message += "使用指令[出售 编号 数量]可以出售背包中的鱼\n"
        return message
