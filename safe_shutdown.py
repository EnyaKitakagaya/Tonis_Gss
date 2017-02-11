#!/usr/bin/env python
# -*- coding: utf-8 -*-

# このスクリプトは、/etc/rc.local に次の２行を追加して自動起動されるべき。
# /usr/bin/python /home/pi/Tonis_Gss/safe_shutdown.py &
# /usr/bin/python /home/pi/Tonis_Gss/startup.py &

import RPi.GPIO as GPIO
import os
import spidev
import time
import loled # OLED ディスプレー表示ライブラリ（自作簡易版）

GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.IN)

button_previous = 1
button_current = 1
brojac = 0
flag_pressed = 0

while True:
    button_current = GPIO.input(5)
    flag_pressed = button_previous + button_current
    if (not(flag_pressed)):
        brojac += 1
    else:
        brojac = 0

    if(button_current and (not button_previous)):
        # print "shutdown -r"
        oled = loled.oled(0)
        oled.write_word("reboot")
        os.system("sudo shutdown -r now")
    if((not flag_pressed) and brojac >= 100):
        # print "shutdown -h"
        oled = loled.oled(0)
        oled.write_word("shutdown -h now")
        os.system("sudo shutdown -h now")
        break

    button_previous = button_current
    time.sleep(0.03)
GPIO.cleanup()
