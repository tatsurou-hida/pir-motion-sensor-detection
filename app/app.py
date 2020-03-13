# -*- coding: utf-8 -*-
'''
Created on 2020/03/03

@author: hida
'''

import traceback
from functools import wraps
import time
import RPi.GPIO as GPIO
from datetime import datetime
import slackweb

def wrapper(func):
    @wraps(func)
    def _func(*args, **keywords):
        try:
            func(*args, **keywords)
        except Exception:
            traceback.print_exc()

    return _func


@wrapper
def log(message):
    print("[" + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ']: ' + message)

@wrapper
def sendToSlack(message):
    log("sending message to slack... message=[" + message + "]")
    slack = slackweb.Slack(url="https://hooks.slack.com/services/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")
    slack.notify(text=message)

@wrapper
def main():
    sensor_pin = 18
    sleeptime = 10

    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sensor_pin, GPIO.IN)

    try:
        log("app start")
        log("ctrl+c  :  if you want to stop the app")
        sendToSlack("detection app started")
        while True:
            if (GPIO.input(sensor_pin) == GPIO.HIGH):
                log("high")
                sendToSlack("PIR motion sensor detected")
                time.sleep(sleeptime)

            else:
                log("low")
                time.sleep(1)
    except KeyboardInterrupt:
        log("stop")
        sendToSlack("detection app stopped")
    finally:
        log("clean up")
        GPIO.cleanup()

if __name__ == '__main__':
    main()
