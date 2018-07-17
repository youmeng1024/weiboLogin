#!/usr/bin/env python
# encoding: utf-8

import requests
import time
import json
import base64
import rsa
import binascii
import random


def preLogin(cookie,username):
    preurl = "https://login.sina.com.cn/sso/prelogin.php"
    preData = {"entry": "account", "callback": "sinaSSOController.preloginCallBack", "su": base64.encodestring(username).strip(), "rsakt": "mod",
               "client": "ssologin.js(v1.4.15)", "_": int(round(time.time() * 1000))}

    response = requests.get(preurl,params=preData,cookies=cookie)
    ret = response.text
    offStart = ret.find('{')
    offEnd = ret.find('}')
    tmp = ret[offStart:offEnd+1]
    js = json.loads(tmp)
    return js




def setData(preJson,username,password):
    postData ={
        "entry": "account",
        "gateway": "1",
        "from": "null",
        "savestate": "30",
        "useticket": "0",
        "pagerefer": "",
        "vsnf": "1",
        "su": base64.encodestring(username).strip(),
        "service": "account",
        "servertime": int(time.time()),
        "nonce": preJson['nonce'],
        "pwencode": "rsa2",
        "rsakv": preJson['rsakv'],
        "sp": "",
        "sr": "1920*1080",
        "encoding": "UTF-8",
        "cdult": "3",
        "domain": "sina.com.cn",
        "prelt": "353",
        "returntype": "TEXT",

    }

    rsaPubKey  = int(preJson['pubkey'],16)
    RSAKEY = rsa.PublicKey(rsaPubKey,int("10001",16))
    enStr = str(postData['servertime']) + '\t' + str(preJson['nonce']) + '\n' + password
    pwd = rsa.encrypt(enStr,RSAKEY)
    postData['sp'] = binascii.b2a_hex(pwd)
    return postData


def req_Image(cookiesss):
    imgurl = "https://login.sina.com.cn/cgi/pin.php"
    imgDic = {
        "r": random.randint(1, 100000000),
        "s": "0"
    }
    imgSavePath = "/home/youmeng/音乐/yan.png"
    imgResult = requests.get(imgurl, params=imgDic, cookies=cookiesss)
    with open(imgSavePath, 'wb') as f:
        f.write(imgResult.content)
    for key in imgResult.cookies.keys():
        cookie[key] = imgResult.cookies.get(key)



def loginPost(cookie,psData):
    #个人新浪中心登录地址
    #https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)&_=1531729547875



    pstUrl = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)&_=%s" %str(int(round(time.time() * 1000)))

    response = requests.post(pstUrl,data=psData,cookies=cookie)
    loginJson  = response.json()

    if loginJson['retcode'] == "0":
        print "login success:",response.text
        print response.headers
        return 0
    elif loginJson['retcode'] == "4049" or loginJson['retcode'] == "2070":
        print "验证码问题"
        print response.text
        return 1
    else:
        print "未知问题"
        print response.text
        return -1


def checkUser(cookie,username):
    #检测帐号，无实际用途
    checkUrl = "https://login.sina.com.cn/bindmail/checkmailuser.php?_r=%d" % int(round(time.time() * 1000))
    checkData = {
        'name': username,
        'type': 'json',
        'ag': ''
    }
    r = requests.post(url=checkUrl, data=checkData, cookies=cookie)




username = ""
password  =""

cookie = {#cookie记录
}



req_Image(cookie)
checkUser(cookie,username)
js = preLogin(cookie,username)
data = setData(js,username,password)

while(True):
    ret = loginPost(cookie,data)
    if ret == 1:
        req_Image(cookie)
        door = raw_input("输入验证码:")
        data = setData(js,username,password)
        data['door'] = door
    else:
        break