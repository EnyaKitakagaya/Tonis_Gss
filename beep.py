#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

buzpin = 23
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(buzpin,GPIO.OUT)

def beep(cnt):
    for i in range(cnt):
        GPIO.output(buzpin,True)
        time.sleep(0.2)
        GPIO.output(buzpin,False)
        time.sleep(0.2)
beep(2)
