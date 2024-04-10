import sqlite3
from math import exp

class Database:
    def __init__(self,id = None):
        self.userId = id
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS users (userId TEXT PRIMARY KEY, name TEXT, point INTEGER)')
        self.connection.commit()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS rod_levels (userId TEXT PRIMARY KEY, level INTEGER)')
        self.connection.commit()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS pool (fishName TEXT PRIMARY KEY, value INTEGER, count INTEGER, owner TEXT)')

    def close(self):
        self.connection.close()
        
    def checkAccount(self,name):
        if self.userId == None: return
        self.cursor.execute('SELECT * FROM users WHERE userId = ?', (self.userId,))
        if len(self.cursor.fetchall()) == 0:
            self.cursor.execute('INSERT INTO users (userId, name, point) VALUES (?, ?, ?)', (self.userId ,name, 0))
            self.connection.commit()

    def insertLevel(self, level):
        if self.userId == None: return
        self.cursor.execute('INSERT INTO rod_levels (userId, level) VALUES (?, ?)', (self.userId, level))
        self.connection.commit()

    def increaseLevel(self):
        if self.userId == None: return
        level = self.selectLevel(self.userId)
        pointNeeded = int(exp(level-1)*20)
        self.cursor.execute('UPDATE users SET point = point - ? WHERE userId = ?', (pointNeeded, self.userId))
        self.cursor.execute('UPDATE rod_levels SET level = level + 1 WHERE userId = ?', (self.userId,))
        self.connection.commit()

    def insertFish(self, fishName, value, count):
        if self.userId == None: return
        self.cursor.execute('INSERT INTO pool (fishName, value, count, owner) VALUES (?, ?, ?, ?)', (fishName, value, count, self.userId))
        self.connection.commit()

    def reduceFish(self, fishName):
        self.cursor.execute('UPDATE pool SET count = count - 1 WHERE fishName = ?', (fishName,))
        self.connection.commit()
        if self.cursor.execute('SELECT count FROM pool WHERE fishName = ?', (fishName,)).fetchone()[0] == 0:
            self.cursor.execute('DELETE FROM pool WHERE fishName = ?', (fishName,))
            self.connection.commit()

    def selectFishOwner(self, fishName):
        self.cursor.execute('SELECT owner FROM pool WHERE fishName = ?', (fishName,))
        result = self.cursor.fetchall()
        if len(result) == 0: return None, None
        userId = result[0][0]
        self.cursor.execute('SELECT name FROM users WHERE userId = ?', (userId,))
        return userId,self.cursor.fetchall()[0][0]
    
    def selectUser(self):
        if self.userId == None: return
        self.cursor.execute('SELECT * FROM users WHERE userId = ?', (self.userId,))
        return self.cursor.fetchall()
    
    def selectAllUser(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

    def selectPool(self):
        self.cursor.execute('SELECT * FROM pool')
        return self.cursor.fetchall()

    def selectPoint(self):
        if self.userId == None: return
        self.cursor.execute('SELECT point FROM users WHERE userId = ?', (self.userId,))
        return self.cursor.fetchall()[0][0]
    
    def changePoint(self, point):
        if self.userId == None: return
        self.cursor.execute('UPDATE users SET point = point + ? WHERE userId = ?', (point, self.userId))
        self.connection.commit()
    
    def selectLevel(self):
        if self.userId == None: return
        if len(self.cursor.execute('SELECT * FROM rod_levels WHERE userId = ?', (self.userId,)).fetchall()) == 0:
            self.insertLevel(1)
        self.cursor.execute('SELECT * FROM rod_levels WHERE userId = ?', (self.userId,))
        return self.cursor.fetchall()[0][1]
    
    def selectAllLevel(self):
        self.cursor.execute('SELECT * FROM rod_levels')
        return self.cursor.fetchall()