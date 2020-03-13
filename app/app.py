# coding: utf-8
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
import configparser
import os

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
def sendToSlack(message, url):
    log("sending message to slack... message=[" + message + "]")
    slack = slackweb.Slack(url=url)
    slack.notify(text=message)

@wrapper
def main():
    sensor_pin = 18
    sleeptime = 10

    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'config.ini'), encoding='utf-8')
    webhook_url = config.get('Slack', 'webhook_url')

    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sensor_pin, GPIO.IN)

    try:
        log("app start")
        log("ctrl+c  :  if you want to stop the app")
        sendToSlack("detection app started", webhook_url)
        while True:
            if (GPIO.input(sensor_pin) == GPIO.HIGH):
                log("high")
                sendToSlack("PIR motion sensor detected", webhook_url)
                time.sleep(sleeptime)

            else:
                log("low")
                time.sleep(1)
    except KeyboardInterrupt:
        log("stop")
        sendToSlack("detection app stopped", webhook_url)
    finally:
        log("clean up")
        GPIO.cleanup()

if __name__ == '__main__':
    main()
