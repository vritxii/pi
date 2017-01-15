import RPi.GPIO as GPIO
from robot import robot
from sound import *
import time, os
from face import face
from alarm import *

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)  #继电器

GPIO_TRIGGER = 16
GPIO_ECHO = 18
GPIO.setwarnings(False)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


def dis():
    GPIO.output(GPIO_TRIGGER, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, GPIO.LOW)
    start = stop = 0
    while GPIO.input(GPIO_ECHO) == 0:
        start = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        stop = time.time()

    elapsed = stop - start
    distance = elapsed * 34300
    distance = distance / 2
    print("Distance : %.1fcm" % distance)
    if distance < 20:
        return True
    else:
        return False


def detect():
    try:
        while True:
            if dis():
                print("请说暗号")
                speak('anhao.mp3')
                b = False
                for i in range(1, 4):
                    filename = record_wave()
                    try:
                        b = robot(filename, i)
                    except:
                        print('No record')
                        speak('yuyin_error.mp3')
                        if i==3:
                            beep()
                        continue
                    print('b=%s' % b)
                    if b == -1:
                        speak('end_chat.mp3')
                        break
                    if b:
                        print('进行人脸识别')
                        speak('face.mp3')
                        k = 0
                        while k < 3:
                            try:
                                if face():
                                    speak('wel.mp3')
                                    print('开门')
                                    open_door()
                                    speak('close.mp3')
                                    break
                                else:
                                    if(k==2):
                                        send_email()
                                        beep()
                                    else:
                                        print('No this persion')
                                        speak('face_error.mp3')
                            except:
                                if(k==2):
                                    send_email()
                                    beep()
                                else:
                                    print('No pic')
                                    speak('face_error.mp3')
                            k += 1
                        break
                        
                    elif b != -1:
                        print('暗号错误')
                        speak('yuyin_error.mp3')
                        if i==3:
                            beep()

            else:
                print("Nobody!")
            time.sleep(1)
    except KeyboardInterrupt:
        print("All Cleanup!")
        GPIO.cleanup()
        os.system('raspi-gpio set 3 op')


def open_door():
    print('hello, welcome come back')
    GPIO.output(8, GPIO.HIGH)
    print('rember close the door')
    time.sleep(5)
    GPIO.output(8, GPIO.LOW)

if __name__ == '__main__':
    detect()
