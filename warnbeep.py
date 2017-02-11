#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

buzpin = 23
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(buzpin,GPIO.OUT)

def warnbeep(cnt):
    for i in range(cnt):
        GPIO.output(buzpin,True)
        time.sleep(0.1)
        GPIO.output(buzpin,False)
        time.sleep(0.1)

warnbeep(5)
