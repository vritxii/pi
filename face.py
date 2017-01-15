# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw
import os, json
faces = ('3f55ee8e0f20d168ded62b3f9dfca57a', '98328d20806d55d00b0e75c827ec6618', '7e66a41a9b9f6a558246a58830ef2294') 

def make_regalur_image(img, size=(256, 256)):
    return img.resize(size).convert('RGB')


def split_image(img, part_size=(64, 64)):
    w, h = img.size
    pw, ph = part_size

    assert w % pw == h % ph == 0

    return [img.crop((i, j, i + pw, j + ph)).copy() \
            for i in range(0, w, pw) \
            for j in range(0, h, ph)]


def hist_similar(lh, rh):
    assert len(lh) == len(rh)
    return sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r)) for l, r in zip(lh, rh)) / len(lh)


def calc_similar(li, ri):
    #   return hist_similar(li.histogram(), ri.histogram())
    return sum(hist_similar(l.histogram(), r.histogram()) for l, r in zip(split_image(li), split_image(ri))) / 16.0


def calc_similar_by_path(lf, rf):
    li, ri = make_regalur_image(Image.open(lf)), make_regalur_image(Image.open(rf))
    return calc_similar(li, ri)


def make_doc_data(lf, rf):
    li, ri = make_regalur_image(Image.open(lf)), make_regalur_image(Image.open(rf))
    li.save(lf + '_regalur.png')
    ri.save(rf + '_regalur.png')
    fd = open('stat.csv', 'w')
    fd.write('\n'.join(l + ',' + r for l, r in zip(map(str, li.histogram()), map(str, ri.histogram()))))
    #   print >>fd, '\n'
    #   fd.write(','.join(map(str, ri.histogram())))
    fd.close()
    li = li.convert('RGB')
    draw = ImageDraw.Draw(li)
    for i in range(0, 256, 64):
        draw.line((0, i, 256, i), fill='#ff0000')
        draw.line((i, 0, i, 256), fill='#ff0000')
    li.save(lf + '_lines.png')


def get_face_token(img_file):
    s="curl -X POST 'https://api-cn.faceplusplus.com/facepp/v3/detect' \
        -F 'api_key=ULMkOR2ixs4zLTIGz_5u0Tnj6yvpETd2' \
        -F 'api_secret=tOmHvb1WPT6eCydDIQ3xrUfVmkK1V1sW' \
        -F 'image_file=@%s/%s' \
        -F 'return_landmark=1' \
        -F 'return_attributes=gender,age'" % (os.getcwd(), img_file)
    os.system('%s > %s/ans.json' % (s, os.getcwd()))
    file = open('ans.json','rb')

    text = file.read()
    #print(text)
    text=text.decode('utf-8')
    #print(text)
    data = json.loads(text)
    print(data['faces'][0]['face_token'])
    return data['faces'][0]['face_token']

def face_plus_plus(i, p):
    #os.system('sh %s/face.sh > %s/ans.json' % (os.getcwd(), os.getcwd()))
    cmd = "curl -X POST 'https://api-cn.faceplusplus.com/facepp/v3/compare' \
        -F 'api_key=ULMkOR2ixs4zLTIGz_5u0Tnj6yvpETd2' \
        -F 'api_secret=tOmHvb1WPT6eCydDIQ3xrUfVmkK1V1sW' \
        -F 'face_token1=%s' \
        -F 'face_token2=%s' \\" % (faces[i-1], p)
    os.system('%s > %s/ans.json' % (cmd, os.getcwd()))
    file = open('ans.json', 'rb')
    text = file.read()
    text = text.decode('utf-8')
    data = json.loads(text)

    # print(jsonobj[0]['Memo'])
    file.close()
    os.remove('ans.json')
    try:
        print(data['confidence'])
        return data['confidence']
    except:
        return 0

def face():
    os.system('fswebcam --no-banner -r 560x480 tmp.jpg')
    face_token = get_face_token('tmp.jpg')
    os.remove('tmp.jpg')
    for i in range(1,4):
    	rate = face_plus_plus(i, face_token)
    	print('test_case: %.3f%%' % rate)
    	if rate > 85:
            #os.remove('tmp.jpg')
            return True
    return False


if __name__=='__main__':
    try:
        print(face())
    except:
        print('No person')