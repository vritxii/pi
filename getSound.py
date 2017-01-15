from robot import *;
from alarm import cut_pic;
import os
if __name__=='__main__':
    try:
        #cut_pic()
        #print(calc_similar_by_path('pics/%d.jpg' % 1, '1.jpg') * 100)
        #os.system('python %s/app-console.py %s 200 200 %s' %(os.getcwd(), '/home/vrit/pic/1.jpg', '/home/vrit/Desktop/face.jpg' ))
        tts_main('face.mp3', '哈哈')
        speak('face.mp3')
    except:
        print('Failed')
