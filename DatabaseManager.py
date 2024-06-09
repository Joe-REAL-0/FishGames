import sqlite3
from math import exp
import json

class Database:
    def __init__(self,id = None):
        self.userId = id
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS users (userId TEXT PRIMARY KEY, name TEXT, point INTEGER)')
        self.connection.commit()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS rod_levels (userId TEXT PRIMARY KEY, level INTEGER)')
        self.connection.commit()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS backpack_levels (userId TEXT PRIMARY KEY, level INTEGER)')
        self.connection.commit()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS backpack (userId TEXT, backPackData TEXT)')
        self.connection.commit()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS pool (fishName TEXT, value INTEGER, count INTEGER, owner TEXT)')
        self.connection.commit()

    def close(self):
        self.connection.close()
        
    def checkAccount(self,name):
        if self.userId == None: return
        self.cursor.execute('SELECT * FROM users WHERE userId = ?', (self.userId,))
        if len(self.cursor.fetchall()) == 0:
            self.cursor.execute('INSERT INTO users (userId, name, point) VALUES (?, ?, ?)', (self.userId ,name, 0))
            self.connection.commit()

    # 鱼塘相关

    def updatePool(self, fishData):
        self.cursor.execute('DELETE FROM pool')
        self.connection.commit()
        for data in fishData:
            if data[1] == 0: continue
            self.cursor.execute('INSERT INTO pool (fishName, value, count, owner) VALUES (?, ?, ?, ?)', (data[0], data[1], data[2], data[3]))
            self.connection.commit()

    def insertFish(self, fishName, value):
        if self.userId == None: return
        self.cursor.execute('INSERT INTO pool (fishName, value, count, owner) VALUES (?, ?, ?, ?)', (fishName, value, 50, self.userId))
        self.connection.commit()

    def reduceFish(self, fishName):
        self.cursor.execute('UPDATE pool SET count = count - 1 WHERE fishName = ?', (fishName,))
        self.connection.commit()
        if self.cursor.execute('SELECT count FROM pool WHERE fishName = ?', (fishName,)).fetchone()[0] == 0:
            self.cursor.execute('DELETE FROM pool WHERE fishName = ?', (fishName,))
            self.connection.commit()

    def removeFish(self, fishName):
        self.cursor.execute('DELETE FROM pool WHERE fishName = ?', (fishName,))
        self.connection.commit()

    def selectFishOwner(self, fishName):
        self.cursor.execute('SELECT owner FROM pool WHERE fishName = ?', (fishName,))
        result = self.cursor.fetchall()
        if len(result) == 0: return None, None
        userId = result[0][0]
        self.cursor.execute('SELECT name FROM users WHERE userId = ?', (userId,))
        return userId,self.cursor.fetchall()[0][0]
    
    def selectFish(self,fishName):
        self.cursor.execute('SELECT * FROM pool WHERE fishName = ?', (fishName,))
        return self.cursor.fetchall()

    def selectPool(self):
        self.cursor.execute('SELECT * FROM pool')
        return self.cursor.fetchall()
    
    # 用户信用点变更

    def selectUser(self):
        if self.userId == None: return
        self.cursor.execute('SELECT * FROM users WHERE userId = ?', (self.userId,))
        return self.cursor.fetchall()
    
    def selectAllUser(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

    def selectPoint(self):
        if self.userId == None: return
        self.cursor.execute('SELECT point FROM users WHERE userId = ?', (self.userId,))
        return self.cursor.fetchall()[0][0]
    
    def changePoint(self, point):
        if self.userId == None: return
        self.cursor.execute('UPDATE users SET point = point + ? WHERE userId = ?', (point, self.userId))
        self.connection.commit()

    #鱼竿相关
    
    def selectRodLevel(self):
        if self.userId == None: return
        if len(self.cursor.execute('SELECT * FROM rod_levels WHERE userId = ?', (self.userId,)).fetchall()) == 0:
            self.insertRodLevel(1)
        self.cursor.execute('SELECT * FROM rod_levels WHERE userId = ?', (self.userId,))
        return self.cursor.fetchall()[0][1]
    
    def selectAllRodLevel(self):
        self.cursor.execute('SELECT * FROM rod_levels')
        return self.cursor.fetchall()
    
    def insertRodLevel(self, level):
        if self.userId == None: return
        self.cursor.execute('INSERT INTO rod_levels (userId, level) VALUES (?, ?)', (self.userId, level))
        self.connection.commit()

    def increaseRodLevel(self):
        if self.userId == None: return
        level = self.selectRodLevel()
        pointNeeded = int(exp(level-1)*20)
        self.cursor.execute('UPDATE users SET point = point - ? WHERE userId = ?', (pointNeeded, self.userId))
        self.cursor.execute('UPDATE rod_levels SET level = level + 1 WHERE userId = ?', (self.userId,))
        self.connection.commit()
    
    #背包相关

    def updateBackpack(self, backPackData):
        if self.userId == None: return
        dataString = json.dumps(backPackData)
        self.cursor.execute('UPDATE backpack SET backPackData = ? WHERE userId = ?', (dataString, self.userId))
        self.connection.commit()
    
    def selectBackpackLevel(self):
        if self.userId == None: return
        if len(self.cursor.execute('SELECT * FROM backpack_levels WHERE userId = ?', (self.userId,)).fetchall()) == 0:
            self.insertBackpackLevel(1)
        self.cursor.execute('SELECT * FROM backpack_levels WHERE userId = ?', (self.userId,))
        return self.cursor.fetchall()[0][1]
    
    def selectAllBackpackLevel(self):
        self.cursor.execute('SELECT * FROM backpack_levels')
        return self.cursor.fetchall()
    
    def insertBackpackLevel(self, level):
        if self.userId == None: return
        self.cursor.execute('INSERT INTO backpack_levels (userId, level) VALUES (?, ?)', (self.userId, level))
        self.connection.commit()
    
    def increaseBackpackLevel(self):
        if self.userId == None: return
        level = self.selectBackpackLevel()
        pointNeeded = int((2.5**level) * 15)
        self.cursor.execute('UPDATE users SET point = point - ? WHERE userId = ?', (pointNeeded, self.userId))
        self.cursor.execute('UPDATE backpack_levels SET level = level + 1 WHERE userId = ?', (self.userId,))
        self.connection.commit()

    def selectBackpack(self):
        if self.userId == None: return
        self.cursor.execute('SELECT * FROM backpack WHERE userId = ?', (self.userId,))
        result = self.cursor.fetchall()
        if len(result) == 0:
            self.cursor.execute('INSERT INTO backpack (userId, backPackData) VALUES (?, ?)', (self.userId, '[]'))
            self.connection.commit()
            return []
        dataString = result[0][1]
        data = json.loads(dataString)
        return data