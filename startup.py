#!/usr/bin/env python
# -*- coding: utf-8 -*-
# このスクリプトは、/etc/rc.local に次の２行を追加して自動起動されるべき。
# /usr/bin/python /home/pi/Tonis_Gss/safe_shutdown.py &
# /usr/bin/python /home/pi/Tonis_Gss/startup.py &
#
import RPi.GPIO as GPIO
import time
import os
#import subprocess
import loled # OLED ディスプレー表示ライブラリ（自作簡易版）

GPIO.setmode(GPIO.BCM)
GPIO.setup(6,GPIO.IN)
GPIO.setup(26,GPIO.IN)


# SW=ON のときTrue
sw1 = not GPIO.input(6)
sw2 = not GPIO.input(26)


if (sw1==True and sw2==False):
    os.system("/usr/bin/python /home/pi/Tonis_Gss/cardtouroku.py")
elif(sw1==True and sw2==True):
    os.system("/usr/bin/python /home/pi/Tonis_Gss/cardtouroku_chk.py")
elif(sw1==False and sw2==False):
    os.system("/usr/bin/python /home/pi/Tonis_Gss/chk_gate_gss2.py")
else:
    oled = loled.oled(0)
    oled.write_word("Maintenance mode.")
