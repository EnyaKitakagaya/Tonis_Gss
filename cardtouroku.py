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
#bell = "/usr/local/bin/Tonis/bell.wav"
beep = "/usr/local/bin/Tonis/beep.py"

# フェリカカードを読んだとき実行
def getid(tag):
    global id
    a = '%s' % tag
    id = "#" + re.findall("ID=([0-9A-F]*)",a)[0]
    os.system("python " + beep + " &") 

clf = nfc.ContactlessFrontend('usb')


# メインループ
oled = loled.oled(0)
print "フェリカカードを登録します"
oled.write_word("Registration mode")
json_key = json.load(open(jsonkey))
scope = ['https://spreadsheets.google.com/feeds']
credentials = oauth2client.client.SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
gc = gspread.authorize(credentials) # google スプレッドシートをオープン
wb = gc.open(wb_name) # ワークブックをオープン 
test1 = wb.worksheet(master_sheet_name) # 会員マスターシートをオープン

# 先ず、最後の会員番号を調べる
criteria_re = re.compile(r'#[0-9]{3}$')
cell_list = test1.findall(criteria_re)
last_userid = cell_list[-1].value
last_userid_no = int(last_userid[1:])
i = last_userid_no +1
oled.clear()
while (True):
    oled.clear()
    oled.write_word("Place card no #%03d" % i)
    # フェリカカード読み込み
    clf.connect(rdwr={'on-connect': getid})
    cardid = id
    master = np.array(test1.get_all_values())
    now = dt.datetime.now().strftime('%Y/%m/%d %X')
    try:
        hit_row_number = np.where(master == id)[0][0] # フェリカIDでマスターシートを検索
        hit_row = master[hit_row_number]
        userid = hit_row[userid_col_no]
        oled.clear()
        oled.write_word("Already registered!!")
    except:
        userid = "#%03d" % i
        test1.append_row([userid,id])
        oled.clear() 
        oled.write_word("id=%s" % userid + " :OK")
        i = i+1
    time.sleep(2)
