#!/usr/bin/env python
#-*-coding:utf-8-*-
# 20170524 Rebeta F.
import os
import sys
import time
import json   #json库
import urllib #网页库
import base64 #Base64加密库
import qrcode #二维码库
import ctypes #printGreen所需库文件
from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics #引入字体库
from reportlab.pdfbase.ttfonts import TTFont #引入字体库
pdfmetrics.registerFont(TTFont('msyh', 'msyh.ttf'))#注册字体


#fileExt = filename[:filename.rindex('.')]

#生成PDF函数
def info2pdf(nameInfo,timeInfo,titleInfo,codeInfo):
    Background = 'background.png'
    Explain = 'explain.png'
    filedir = "./" + time.strftime('%Y%m%d',time.localtime(time.time())) + "/" #按照时间生成目录
    isExists = os.path.exists(filedir) #判断目录是否存在
    if not isExists:
        os.mkdir(filedir) #不存在目录就创建新目录
    filename = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + '.pdf' #按照时间生成文件名
    fileExt = filedir + filename #拼合目录及文件名
    (w, h) = portrait(A4)
    c = canvas.Canvas(fileExt, pagesize = portrait(A4))
    c.setTitle('用稿通知 - 忻州师范学院招生就业处 · 掌上忻师') #设置标题
    c.drawImage(Background, 0, 0, w, h) #绘制证书背景图案
    qr = qrcode.QRCode(  #设置二维码生成参数
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=0.1,
        )
    qr.add_data(base64.b64encode(codeInfo))
    qr.make(fit=True)
    img = qr.make_image() #生成防伪验证码
    img.save("temp.png")  #保存防伪验证码
    c.drawImage("temp.png", 260, 230, 74, 74) #绘制防伪验证码
    c.setFont("msyh", 20) #设置字体
    c.drawString(100,596,nameInfo[0:1] + " " + nameInfo[1:2] + " " + nameInfo[2:3] + " " + nameInfo[3:4]) #绘制姓名
    c.setFont("msyh", 22) #重设字体
    c.drawString(435,522,timeInfo[0:4])#绘制用稿时间(年)
    c.drawString(100,487,timeInfo[5:7])  #绘制用稿时间(月)
    c.drawString(150,487,timeInfo[8:10])  #绘制用稿时间(日)
    c.setFont("msyh", 16) #重设字体
    c.drawString(180,345,"《"+ titleInfo +"》") #绘制稿件标题
    c.setFont("msyh", 14) #重设字体
    c.drawString(285,196,codeInfo) #绘制证书编号
    c.setFont("msyh", 18) #重设字体
    c.drawString(227,145,time.strftime('%Y年%m月%d日',time.localtime(time.time())))#绘制打印时间
    c.showPage() #保存上一个画布到页面,并新建一个页面
    c.drawImage(Explain, 0, 0, w, h) #绘制说明
    c.save() #保存到PDF文件
    print time.strftime('%Y/%m/%d %H:%M:%S --> ',time.localtime(time.time())) + "Save File " + filename + " (For:"+ nameInfo +") Success."


result = json.loads(urllib.urlopen("https://api.rebeta.cn/OTHER_ZSInfo_all.php").read()) #取回信息
for res in result:
    info2pdf(res["name"],res["ctime"],res["title"].encode("utf-8"),res["cid"])
