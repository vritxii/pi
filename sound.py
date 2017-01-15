# -*- coding: utf-8 -*-
import os
from datetime import datetime


def speak(sound_file):
    os.system('mpg123 %s' % sound_file)
    '''
    pygame.init()
    pygame.mixer.init()
    pygame.time.delay(10)
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    #time.sleep(5)
    while pygame.mixer.music.get_busy() == False:
        print("hh")
        time.sleep(1)
    time.sleep(3)
    pygame.mixer.init()
    pygame.time.delay(10)
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    time.sleep()
    '''


def record_wave():
    filename = datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + ".wav"
    #os.system('rec -c 1 -e signed-integer -r 16000 -b 16 %(filename)s trim 0 00:5' % {'filename': filename})
    os.system('arecord -r 16000 -f s16_le -D "plughw:1,0" -d 3 %(filename)s' % {'filename': filename})
    return filename
