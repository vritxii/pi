import RPi.GPIO as GPIO
import time
PIN_NO = 5
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_NO, GPIO.OUT)


def beep(seconds):
     GPIO.output(PIN_NO, GPIO.HIGH)
     time.sleep(seconds)
     GPIO.output(PIN_NO, GPIO.LOW)


def beepAction(secs, sleepsecs, times):
    for i in range(times):
        beep(secs)
        time.sleep(sleepsecs)