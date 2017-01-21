#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 参考 http://gspread.readthedocs.io/en/latest/
#
import loled # OLED ディスプレー表示ライブラリ（自作簡易版）
import json
import gspread # google スプレッドシート用のライブラリ
import oauth2client.client
import nfc
import spidev
import re
import os
import time
import datetime as dt
import numpy as np
import sys

wb_name = "FLK_kanri" # ワークブック名

master_sheet_name = "memberList" # 会員マスターシート名
userid_col_no = 0 # 会員番号のカラム番号（ゼロから始まる）
felicaid_col_no = 1 # FelicaIDのカラム番号（ゼロから始まる）

jsonkey = "/home/pi/Tonis-0674cbe9d8cc.json" # シートをアクセスするための認証キー
bell = "/usr/local/bin/Tonis/bell.wav"

# フェリカカードを読んだとき実行
def getid(tag):
    global id
    a = '%s' % tag
    id = "#" + re.findall("ID=([0-9A-F]*)",a)[0]
    os.system("aplay " + bell + " &") 

clf = nfc.ContactlessFrontend('usb')


# メイン
oled = loled.oled(0)
oled.write_word("Registration Check.")
time.sleep(2)
oled.clear()
oled.write_word("Place cards.")
json_key = json.load(open(jsonkey))
scope = ['https://spreadsheets.google.com/feeds']
credentials = oauth2client.client.SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
gc = gspread.authorize(credentials) # google スプレッドシートをオープン
wb = gc.open(wb_name) # ワークブックをオープン 
test1 = wb.worksheet(master_sheet_name) # 会員マスターシートをオープン

while (True):
    # フェリカカード読み込み
    clf.connect(rdwr={'on-connect': getid})
    cardid = id
    # google スプレッドシートのアクセス認証（一定期間アクセス無いと切れてしまうので、毎回認証する）
    json_key = json.load(open(jsonkey))
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = oauth2client.client.SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
    gc = gspread.authorize(credentials)
    # google スプレッドシートをオープン
    wb = gc.open(wb_name) # ワークブックをオープン 
    test1 = wb.worksheet(master_sheet_name) # 会員マスターシートをオープン
    master = np.array(test1.get_all_values())
    try:
        hit_row_number = np.where(master == id)[0][0] # フェリカIDでマスターシートを検索
        hit_row = master[hit_row_number]
        userid = hit_row[userid_col_no]
        oled.clear()
        oled.write_word("userid=%s" % userid)
    except:
        oled.clear()
        oled.write_word("Not Registered!!")
    time.sleep(2)
    
