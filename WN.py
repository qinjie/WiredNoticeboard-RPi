import requests
import json
import urllib
import os
import subprocess
import time
import shutil



import getSerial

def internet_on():
    try:
        request.urlopen('http://128.199.93.67', timeout=1)
        return True
    except request.URLError as err:
        return False

def createFolder():
    if not os.path.exists('Data') :
        os.makedirs('Data')
    if not os.path.exists('Data/Video'):
        os.makedirs('Data/Video')
    if not os.path.exists('Data/Image'):
        os.makedirs('Data/Image')

    if not os.path.exists('Temp') :
        os.makedirs('Temp')
    if not os.path.exists('Temp/Video') :
        os.makedirs('Temp/Video')
    if not os.path.exists('Temp/Image') :
        os.makedirs('Temp/Image')

def get_filepaths(directory):
    file_paths = []  # List which will store all of the full filepaths.

    for root, directories, files in os.walk(directory):
        for filename in files:

            file_paths.append(filename)  # Add it to the list.

    return file_paths

def downloadVideo(link, name) :
    mp3file = urllib.urlopen(link)
    with open("Data/Video/" + name + ".mp4", 'wb') as output:
        output.write(mp3file.read())

def downloadImage(link, name) :
    a = 1
    urllib.urlretrieve(link, "Data/Image/" + name + ".jpg")

def prepareFile() :
    listVideoFile = get_filepaths('Data/Video')

    for a in listVideoFile:
        currentDirectory = 'Data/Video/' + a
        newDirectory  = 'Temp/Video/' + a
        shutil.move(currentDirectory, newDirectory)

    listImageFile = get_filepaths('Data/Image')
    for a in listImageFile:
        currentDirectory = 'Data/Image/' + a
        newDirectory = 'Temp/Image/' + a
        shutil.move(currentDirectory, newDirectory)

def downloadData(data) :
    listVideoName = get_filepaths('Temp/Video')
    listImageName = get_filepaths('Temp/Image')
    for a in data :
        mediaFile = a['mediaFile']
        name = mediaFile['name']
        extension = mediaFile['extension']
        link = mediaFile['link']
        fullname = name + '.' + extension
        if extension == 'jpg' :
            currentDirectory = 'Temp/Image/' + fullname
            newDirectory = 'Data/Image/' + fullname
            if fullname in listImageName :
                shutil.move(currentDirectory, newDirectory)
            else :
                downloadImage(link, name)
        else :
            currentDirectory = 'Temp/Video/' + fullname
            newDirectory = 'Data/Video/' + fullname
            if fullname in listVideoName:
                shutil.move(currentDirectory, newDirectory)
            else:
                downloadVideo(link, name)

def batch() :
    url  = "http://128.199.93.67/WiredNoticeboard-Web/api/web/index.php/v1/device/get-device"
    token = getSerial.getserial()
    post_data = {'token': token}
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
        downloadData(data)
        for a in data :
            iteration = a['iteration']
            mediaFile = a['mediaFile']
            name = mediaFile['name']
            extension = mediaFile['extension']
            for i in range(0, iteration) :
                if extension == 'jpg':
                    subprocess.call(["fbi", "-a", "-T", "1", "Data/Image/" + name + ".jpg"])
                    time.sleep(5)
                    subprocess.call(["pkill", "fbi"])
                else :
                    subprocess.call(["omxplayer", "Data/Video/" + name + ".mp4"])

if __name__ == "__main__" :
    createFolder()
    prepareFile()
    batch()
    # while (1) :
    #     batch()
