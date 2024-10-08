from PIL import Image, ImageDraw, ImageFont
from .FishDataManager import FishDataManager
from random import shuffle
from time import time
import os

lastUsedTime = time()

def listFishMain():
    global lastUsedTime
    where=str(os.path.dirname(os.path.abspath(__file__)))+'/'
    if time() - lastUsedTime < 60:
        return "鱼塘大屏指令有一分钟冷却时间！"
    lastUsedTime = time()
    Font1 = ImageFont.truetype(where+'MiSans-Medium.ttf', 60)
    Font2 = ImageFont.truetype(where+'MiSans-Medium.ttf', 40)
    Font3 = ImageFont.truetype(where+'MiSans-Medium.ttf', 30)
    poolData = FishDataManager().fishData
    tp = len(poolData) if len(poolData) <= 20 else 20
    im=Image.new(mode="RGB", size=(1090, 210+85*tp), color="white")
    bk = ImageDraw.Draw(im)
    bk.text((380, 35),text='鱼塘大屏',font=ImageFont.truetype(where+'MiSans-Medium.ttf', 80),fill="#adf5ff")
    bk.text((770, 50), text='总鱼数: ', font=Font2, fill="black")
    if tp == 20 :
        shuffle(poolData)
        bk.text((340, 5),text='当前随机展示池塘内二十种鱼',font=Font3,fill="#eeee16")
        bk.text((900, 50), text=str(len(poolData))+'种', font=Font2, fill="black")
    bk.text((100, 140),text='鱼名',font=Font1,fill="black")
    bk.text((480, 140),text='数量',font=Font1,fill="black")
    bk.text((860, 140),text='价格',font=Font1,fill="black")
    y = 220
    for data in poolData:
        bk.text((100, y), text=str(data[0]), font=Font2, fill="black")
        bk.text((480, y), text=str(data[2]), font=Font2, fill="black")
        bk.text((860, y), text=str(data[1]), font=Font2, fill="black")
        y += 85
    
    place=where + str(time()) + ".jpg"
    im.save(place)
    return place
