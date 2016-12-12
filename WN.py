import requests
import json
import urllib
import os
import subprocess
import time

import urllib2

def internet_on():
    try:
        request.urlopen('http://128.199.93.67', timeout=1)
        return True
    except request.URLError as err:
        return False

def createFolder():
    if not os.path.exists('Video'):
        os.makedirs('Video')

    if not os.path.exists('Image'):
        os.makedirs('Image')

def downloadVideo(link, name) :
    mp3file = urllib.urlopen(link)
    with open("Video/" + name + ".mp4", 'wb') as output:
        output.write(mp3file.read())

def downloadImage(link, name) :
    a = 1
    urllib.urlretrieve(link, "Image/" + name + ".jpg")

def batch() :
    url  = "http://128.199.93.67/WiredNoticeboard-Web/api/web/index.php/v1/device/get-device"
    post_data = {'token': 'abc'}
    get_response = requests.post(url=url, data=post_data)
    data = json.loads(get_response.text)
    if (get_response.text == '-1') :
        print('This device does not register!')
    else :
        print(data)
        auth = "Bearer " + data['token']
        device_id = data['device_id']
        print(auth)
        url = "http://128.199.93.67/WiredNoticeboard-Web/api/web/index.php/v1/device-media/get-media"
        headers = {'Authorization': '%s' % auth}
        post_data = {'device_id' : device_id}
        get_response = requests.get(url, data=post_data, headers=headers)
        data = json.loads(get_response.text)
        for a in data :
            mediaFile = a['mediaFile']
            name = mediaFile['name']
            extension = mediaFile['extension']
            duration = mediaFile['duration']
            link = mediaFile['link']
            if extension == 'jpg' :
                downloadImage(link, name)
            else:
                downloadVideo(link, name)

            for i in range(0, duration) :
                if extension == 'jpg':
                    subprocess.call(["fbi", "-a", "-T", "1", "Image/" + name + ".jpg"])
                    time.sleep(5)
                else :
                    subprocess.call(["omxplayer", "Video/" + name + ".mp4"])

if __name__ == "__main__" :
    createFolder()
    batch()
