import pymysql
from math import exp
import json

class Database:
    host = 'localhost'
    port = 3306
    user = "root"
    password = "password"
    dbName = 'fishing_game'

    def __init__(self,id = None):
        self.userId = id

        #建立连接
        self.connection = pymysql.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.password
        )

        #检查数据库
        self.cursor = self.connection.cursor()
        self.cursor.execute(f'CREATE DATABASE IF NOT EXISTS {self.dbName}')
        self.connection.commit()

        #连接数据库
        self.connection.database = self.dbName

        #设置操作游标并检查表
        self.cursor = self.connection.cursor(prepared = True)
        self.cursor.execute('CREATE TABLE IF NOT EXISTS users (userId VARCHAR(32) PRIMARY KEY, name TEXT, point INTEGER)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS rod_levels (userId VARCHAR(32) PRIMARY KEY, level INTEGER)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS backpack_levels (userId VARCHAR(32) PRIMARY KEY, level INTEGER)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS backpack (userId VARCHAR(32) PRIMARY KEY, backPackData TEXT)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS pool (fishName TEXT, value INTEGER, count INTEGER, owner TEXT)')
        self.connection.commit()

    def close(self):
        self.connection.close()
        
    def checkAccount(self,name):
        if self.userId == None: return
        self.cursor.execute('SELECT * FROM users WHERE userId = %s', (self.userId,))
        if len(self.cursor.fetchall()) == 0:
            self.cursor.execute('INSERT INTO users (userId, name, point) VALUES (%s, %s, %s)', (self.userId ,name, 0))
            self.cursor.execute('INSERT INTO rod_levels (userId, level) VALUES (%s, %s)', (self.userId, 1))
            self.cursor.execute('INSERT INTO backpack_levels (userId, level) VALUES (%s, %s)', (self.userId, 1))
            self.connection.commit()

    # 鱼塘相关

    def updatePool(self, fishData):
        self.cursor.execute('DELETE FROM pool')
        for data in fishData:
            if data[1] == 0: continue
            self.cursor.execute('INSERT INTO pool (fishName, value, count, owner) VALUES (%s, %s, %s, %s)', (data[0], data[1], data[2], data[3]))
        self.connection.commit()

    def insertFish(self, fishName, value):
        if self.userId == None: return
        self.cursor.execute('INSERT INTO pool (fishName, value, count, owner) VALUES (%s, %s, %s, %s)', (fishName, value, 50, self.userId))
        self.connection.commit()

    def reduceFish(self, fishName):
        self.cursor.execute('UPDATE pool SET count = count - 1 WHERE fishName = %s', (fishName,))
        if self.cursor.execute('SELECT count FROM pool WHERE fishName = %s', (fishName,)).fetchone()[0] == 0:
            self.cursor.execute('DELETE FROM pool WHERE fishName = %s', (fishName,))
        self.connection.commit()

    def removeFish(self, fishName):
        self.cursor.execute('DELETE FROM pool WHERE fishName = %s', (fishName,))
        self.connection.commit()

    def selectFishOwner(self, fishName):
        self.cursor.execute('SELECT owner FROM pool WHERE fishName = %s', (fishName,))
        result = self.cursor.fetchall()
        if len(result) == 0: return None, None
        userId = result[0][0]
        self.cursor.execute('SELECT name FROM users WHERE userId = %s', (userId,))
        return userId,self.cursor.fetchall()[0][0]
    
    def selectFish(self,fishName):
        self.cursor.execute('SELECT * FROM pool WHERE fishName = %s', (fishName,))
        return self.cursor.fetchall()

    def selectPool(self):
        self.cursor.execute('SELECT * FROM pool')
        return self.cursor.fetchall()
    
    # 用户信用点变更

    def selectUser(self):
        if self.userId == None: return
        self.cursor.execute('SELECT * FROM users WHERE userId = %s', (self.userId,))
        return self.cursor.fetchall()
    
    def selectAllUser(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

    def selectPoint(self):
        if self.userId == None: return
        self.cursor.execute('SELECT point FROM users WHERE userId = %s', (self.userId,))
        return self.cursor.fetchall()[0][0]
    
    def changePoint(self, point):
        if self.userId == None: return
        self.cursor.execute('UPDATE users SET point = point + %s WHERE userId = %s', (point, self.userId))
        self.connection.commit()

    #鱼竿相关
    
    def selectRodLevel(self):
        if self.userId == None: return
        self.cursor.execute('SELECT * FROM rod_levels WHERE userId = %s', (self.userId,))
        if len(self.cursor.fetchall()) == 0:
            self.insertRodLevel(1)
        self.cursor.execute('SELECT * FROM rod_levels WHERE userId = %s', (self.userId,))
        return self.cursor.fetchall()[0][1]
    
    def selectAllRodLevel(self):
        self.cursor.execute('SELECT * FROM rod_levels')
        return self.cursor.fetchall()
    
    def insertRodLevel(self, level):
        if self.userId == None: return
        self.cursor.execute('INSERT INTO rod_levels (userId, level) VALUES (%s, %s)', (self.userId, level))
        self.connection.commit()

    def increaseRodLevel(self):
        if self.userId == None: return
        level = self.selectRodLevel()
        pointNeeded = int(exp(level-1)*20)
        self.cursor.execute('UPDATE users SET point = point - %s WHERE userId = %s', (pointNeeded, self.userId))
        self.cursor.execute('UPDATE rod_levels SET level = level + 1 WHERE userId = %s', (self.userId,))
        self.connection.commit()
    
    #背包相关

    def updateBackpack(self, backPackData):
        if self.userId == None: return
        dataString = json.dumps(backPackData)
        self.cursor.execute('UPDATE backpack SET backPackData = %s WHERE userId = %s', (dataString, self.userId))
        self.connection.commit()
    
    def selectBackpackLevel(self):
        if self.userId == None: return
        self.cursor.execute('SELECT * FROM backpack_levels WHERE userId = %s', (self.userId,))
        if len(self.cursor.fetchall()) == 0:
            self.insertBackpackLevel(1)
        self.cursor.execute('SELECT * FROM backpack_levels WHERE userId = %s', (self.userId,))
        return self.cursor.fetchall()[0][1]
    
    def selectAllBackpackLevel(self):
        self.cursor.execute('SELECT * FROM backpack_levels')
        return self.cursor.fetchall()
    
    def insertBackpackLevel(self, level):
        if self.userId == None: return
        self.cursor.execute('INSERT INTO backpack_levels (userId, level) VALUES (%s, %s)', (self.userId, level))
        self.connection.commit()
    
    def increaseBackpackLevel(self):
        if self.userId == None: return
        level = self.selectBackpackLevel()
        pointNeeded = int((2.5**level) * 15)
        self.cursor.execute('UPDATE users SET point = point - %s WHERE userId = %s', (pointNeeded, self.userId))
        self.cursor.execute('UPDATE backpack_levels SET level = level + 1 WHERE userId = %s', (self.userId,))
        self.connection.commit()

    def selectBackpack(self):
        if self.userId == None: return
        self.cursor.execute('SELECT * FROM backpack WHERE userId = %s', (self.userId,))
        result = self.cursor.fetchall()
        if len(result) == 0:
            self.cursor.execute('INSERT INTO backpack (userId, backPackData) VALUES (%s, %s)', (self.userId, '[]'))
            self.connection.commit()
            return []
        dataString = result[0][1]
        data = json.loads(dataString)
        return data