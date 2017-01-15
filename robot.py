# coding: utf-8
import urllib.request
import json
import base64
import sys
import os
from sound import speak, record_wave
from alarm import *

App_ID = "8541844"
API_Key = "u5hXTZKrzijAHxc4Q36UGX7R"
Secret_Key = "8vmQOsxHZKSIanPa4X7Gg9ClkXAI3z9h"


def get_access_token():
    url = "https://openapi.baidu.com/oauth/2.0/token"
    grant_type = "client_credentials"
    client_id = API_Key
    client_secret = Secret_Key

    url = url + "?" + "grant_type=" + grant_type + "&" + "client_id=" + client_id + "&" + "client_secret=" + client_secret

    resp = urllib.request.urlopen(url).read()
    data = json.loads(resp.decode("utf-8"))
    return data["access_token"]


def baidu_asr(data, id, token):
    speech_data = base64.b64encode(data).decode("utf-8")
    speech_length = len(data)
    post_data = {
        "format": "wav",
        "rate": 16000,
        "channel": 1,
        "cuid": id,
        "token": token,
        "speech": speech_data,
        "len": speech_length
    }

    url = "http://vop.baidu.com/server_api"
    json_data = json.dumps(post_data).encode("utf-8")
    json_length = len(json_data)
    #print(json_data)

    req = urllib.request.Request(url, data=json_data)
    req.add_header("Content-Type", "application/json")
    req.add_header("Content-Length", json_length)

    print("asr start request\n")
    resp = urllib.request.urlopen(req)
    print("asr finish request\n")
    resp = resp.read()
    resp_data = json.loads(resp.decode("utf-8"))
    if resp_data["err_no"] == 0:
        return resp_data["result"]
    else:
        print(resp_data)
    return None


def asr_main(filename):
    f = open(filename, "rb")
    audio_data = f.read()
    f.close()
    token = get_access_token()
    uuid = "xxxx"
    resp = baidu_asr(audio_data, uuid, token)
    os.remove(filename)
    print(resp[0])
    return resp[0]


def robot_main(words):
    url = "http://www.tuling123.com/openapi/api?key="

    key = "564db8e609ef446589acb59d096d47cb"

    words = urllib.parse.quote(words)
    url = url + key + "&info=" + words

    req = urllib.request.Request(url)
    req.add_header("apikey", key)

    print("robot start request")
    resp = urllib.request.urlopen(req)
    print("robot stop request")
    content = resp.read()
    if content:
        data = json.loads(content.decode("utf-8"))
        print(data)
        print(data["text"])
        return data["text"]
    else:
        return None


def baidu_tts_by_post(data, id, token):
    post_data = {
        "tex" : data,
        "lan" : "zh",
        "ctp" : 1,
        "cuid" : id,
        "tok" : token,
    }

    url = "http://tsn.baidu.com/text2audio"
    post_data = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request(url, data = post_data)

    print("tts start request")
    resp = urllib.request.urlopen(req)
    print("tts finish request")
    resp = resp.read()
    return resp


def tts_main(filename, words):
    token = get_access_token()
    text = urllib.parse.quote(words)
    uuid = "1000"
    resp = baidu_tts_by_post(text, uuid, token)

    f = open(filename, "wb")
    f.write(resp)
    f.close()


def robot(sound_file, mode):
    b = 0
    print('mode=%d' % mode)
    words = asr_main(sound_file)
    if mode > 0:
        if contain_key(words, '芝麻开门'):
            return True
        elif mode == 3:
            #beep()
            return False
        elif contain_key(words, '聊天'):
            mode = 0
        else:
            return False

    print('Begin chat')
    while b != -1 and mode == 0:
        try:
            if mode == 0 and contain_key(words, '退出'):
                print("exit !")
                b = -1
                return b
            new_words = robot_main(words)
            tts_main("response.mp3", new_words)
            speak('response.mp3')
            os.remove('response.mp3')
            sound_file = record_wave()
            words = asr_main(sound_file)
        except:
            print('No record')
            

def contain_key(a, key):
    try:
        key = key.decode('utf-8')
        a = a.decode('utf-8')
    except:
        print("Need't decode")
    return key in a


def sound_test(mode):
    b = True
    if mode == 0:
        while b:
            filename = record_wave()
            b = robot(filename, 0)
    else:
        for i in range(1, 4):
            filename = record_wave()
            b = robot(filename, i)
    return b
