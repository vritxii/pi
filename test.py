import os
from robot import robot
from sound import *
import time
from face import face


def cut_pic():
    os.system('rm -f *.jpg *.tar.gz')
    for i in range(1, 4):
        os.system('fswebcam --no-banner -r 560x480 %d.jpg' % i)
    os.system('tar -czf all.tar.gz *.jpg')
    os.system('rm -f *.jpg')


def detect():
    try:
        while True:
            a = input('Input')
            if a == '1':
                print("请说暗号")
                b = False
                for i in range(1, 4):
                    filename = record_wave()
                    try:
                        b = robot(filename, i)
                    except:
                        print('No record')
                    print('b=%s' % b)
                    if b == -1:
                        break

                    if b:
                        print('进行人脸识别')
                        try:
                            i = 0
                            while i < 3:
                                if face():
                                    print('开门')
                                    open_door()
                                    break
                                else:
                                    print('No this persion')
                                i += 1
                            break
                        except:
                            print('No pic')
                    elif b != -1:
                        print('暗号错误')


            else:
                print("Nobody!")
            time.sleep(1)
    except KeyboardInterrupt:
        print("All Cleanup!")


def open_door():
    print('Opened the door')
    print('rember close the door')
    time.sleep(6)


if __name__ == '__main__':
    '''
    i = 0
    b = 0
    while b == 0 and i < 5:
        filename = record_wave()
        try:
            b = robot(filename, 0)
        except:
            print('No record')
        os.remove(filename)
        i += 1
    '''
    detect()
    #cut_pic()
    #print(face())

