#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

bell="/usr/local/bin/Tonis/bell.wav"
horn="/usr/local/bin/Tonis/horn.wav"

# グーグルシートの定義
jsonkey = "/home/pi/Tonis-0674cbe9d8cc.json" # シートをアクセスするための認証キー
wb_name = "FLK_kanri" # ワークブック名
master_sheet_name = "memberList" # 会員マスターシート名
userid_col_no = 0       # 会員番号のカラム番号（カラム番号はゼロから始まる）
username_col_no = 2     # ユーザー名（液晶に表示されるペンネーム：半角でないと化ける）のカラム番号
##valid_from_col_no = 5 # 有効開始日（白石さん方式にするので、使用しない）
valid_to_col_no = 7     # 有効期限（白石さん方式にするので、表示のみ）
validity_col_no = 8     # 有効か無効かのデータが入ってるカラムの番号
mail_col_no = 4         # メールアドレスが入っているカラムの番号

log_sheet_name = "entry-exitLog" # ログシート名
dummy_sheet_name = "dummy" # ダミーシート名（状態スイッチを付けるまでの暫定策）

# 入退出メッセージ
in_message = u"\nご利用ありがとうございます。お帰りの際には、忘れずにカードをかざしてください。"
out_message = u"\nお疲れ様でした。またのご利用をお待ちしています。"


# メール
import smtplib
from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import formatdate

def sendmail(from_address, to_address, subject, message):
    charset = 'ISO-2022-JP'
    msg = MIMEText(message.encode(charset), 'plain', charset)
    msg['Subject'] = Header(subject, charset)
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Date'] = formatdate(localtime=True)
    smtp = smtplib.SMTP('localhost')
    smtp.sendmail(from_address, to_address, msg.as_string())
    smtp.close()

# フェリカカードを読んだとき実行
def getid(tag):
    global id
    a = '%s' % tag
    id = "#" + re.findall("ID=([0-9A-F]*)",a)[0]
    os.system("aplay " + bell + " &") 

clf = nfc.ContactlessFrontend('usb')

oled = loled.oled(0)
oled.write_word("Normal mode")
time.sleep(3)


# メインループ
while (True):
    oled.clear()
    oled.write_word("Place your card.")
    #print "会員カードをかざして下さい。"
    # フェリカカード読み込み
    clf.connect(rdwr={'on-connect': getid})
    cardid = id
    # google スプレッドシートのアクセス認証（一定期間アクセス無いと切れてしまうので、毎回認証する）
    json_key = json.load(open(jsonkey))
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = oauth2client.client.SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
    gc = gspread.authorize(credentials)   # google スプレッドシートをオープン
    wb = gc.open(wb_name) # ワークブックをオープン 
    test1 = wb.worksheet(master_sheet_name) # 会員マスターシートをオープン
    log = wb.worksheet(log_sheet_name) # ログシートをオープン
    dummy = wb.worksheet(dummy_sheet_name) # ダミーシートをオープン
    master = np.array(test1.get_all_values())
    now = dt.datetime.now().strftime('%Y/%m/%d %X')
    try:
        hit_row_number = np.where(master == id)[0][0] # フェリカIDでマスターシートを検索
        hit_row = master[hit_row_number]
        userid = hit_row[userid_col_no]
##        valid_from = hit_row[valid_from_col_no]
        valid_to = hit_row[valid_to_col_no]
        validity = hit_row[validity_col_no]
        penname = hit_row[username_col_no]
        mailaddr = hit_row[mail_col_no]
        if (validity != "valid"):
            oled.clear()
            oled.write_word("Kigen Gire or Shikkou!!")
            oled.write_word(" " + valid_to + "  made")
            os.system("aplay " + horn + " &") 
        else:
            all_log = np.array(dummy.get_all_values())
            hit_row_array = np.where(all_log == userid)
            try:
                hit_row_max = max(hit_row_array[0])
                #print hit_row_max
                if (all_log[max(hit_row_array[0])][2] == ""):
                    #print "out"
                    oled.clear()
                    oled.write_word("Bye! ")
                    oled.write_word(penname)
                    dummy.update_cell(hit_row_max +1,3,now)
                    log.append_row([userid,now,"out"])
                    sendmail('nishijim2001@gmail.com', mailaddr, u'ラボ退出しました', penname + u'様' + out_message) 
                else:
                    #print "in"
                    oled.clear()
                    oled.write_word("Hello! ")
                    oled.write_word(penname)
                    dummy.append_row([userid,now])
                    log.append_row([userid,now,"in"])
                    sendmail('nishijim2001@gmail.com', mailaddr, u'ラボ入室しました', penname + u'様' + in_message) 
            except:
                #print "new in"
                oled.clear()
                oled.write_word("Hello! ")
                oled.write_word(penname)
                dummy.append_row([userid,now])
                log.append_row([userid,now,"in"])
                sendmail('nishijim2001@gmail.com', mailaddr, u'ラボ入室しました', penname + u'様' + in_message) 
    except:
        #print "Invalid card 2!!"
        oled.clear()
        oled.write_word("Invalid card !!")
        os.system("aplay " + horn + " &") 
    time.sleep(2)

pi@raspberrypi:/usr/local/bin/Tonis $ 
