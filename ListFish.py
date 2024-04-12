from PIL import Image, ImageDraw, ImageFont
from .DatabaseManager import Database
from time import time

lastUsedTime = time()

def listFishMain():
    global lastUsedTime
    if time() - lastUsedTime < 60:
        return "鱼塘大屏指令有一分钟冷却时间！"
    lastUsedTime = time()
    Font1 = ImageFont.truetype('MiSans.ttf', 60)
    Font2 = ImageFont.truetype('MiSans.ttf', 40)
    Font3 = ImageFont.truetype('MiSans.ttf', 30)
    db = Database()
    poolData = db.selectPool()
    tp = len(poolData) if len(poolData) <= 20 else 20 
    bk = Image.open('bk.png').resize((1090, 210+85*tp))
    drawer = ImageDraw.Draw(bk)
    drawer.text((380, 35),text='鱼塘大屏',font=ImageFont.truetype('MiSans.ttf', 80),fill="#adf5ff")
    if len(poolData)>20 :drawer.text((340, 5),text='当前随机展示池塘内二十种鱼',font=Font3,fill="#eeff00")
    drawer.text((100, 140),text='鱼名',font=Font1,fill="black")
    drawer.text((480, 140),text='数量',font=Font1,fill="black")
    drawer.text((860, 140),text='价格',font=Font1,fill="black")
    y = 220
    for data in poolData:
        drawer.text((100, y), text=str(data[0]), font=Font2, fill="black")
        drawer.text((480, y), text=str(data[1]), font=Font2, fill="black")
        drawer.text((860, y), text=str(data[2]), font=Font2, fill="black")
        y += 85
    return bk