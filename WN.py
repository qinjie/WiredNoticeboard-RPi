import requests
import json
import urllib
import os
import subprocess
import time
import shutil
import pygame

import rpiSerial

def internet_on():
    try:
        requests.urlopen('http://128.199.93.67', timeout=1)
        return True
    except requests.URLError as err:
        return False

def createFolder():
<<<<<<< HEAD
    if not os.path.exists('Data') :
        os.makedirs('Data')
    if not os.path.exists('Data/Video'):
        os.makedirs('Data/Video')
    if not os.path.exists('Data/Image'):
        os.makedirs('Data/Image')
    if not os.path.exists('Data/pptx') :
        os.makedirs('Data/pptx')

    if not os.path.exists('Temp') :
        os.makedirs('Temp')
    if not os.path.exists('Temp/Video') :
        os.makedirs('Temp/Video')
    if not os.path.exists('Temp/Image') :
        os.makedirs('Temp/Image')
    if not os.path.exists('Temp/pptx') :
        os.makedirs('Temp/pptx')
=======
    if not os.path.exists('data') :
        os.makedirs('data')
    if not os.path.exists('data/video'):
        os.makedirs('data/video')
    if not os.path.exists('data/image'):
        os.makedirs('data/image')

    if not os.path.exists('Temp') :
        os.makedirs('Temp')
    if not os.path.exists('Temp/video') :
        os.makedirs('Temp/video')
    if not os.path.exists('Temp/image') :
        os.makedirs('Temp/image')
>>>>>>> 5300069628d81c512c892f6b69e6d970216ca3d7

def get_filepaths(directory):
    file_paths = []  # List which will store all of the full filepaths.

    for root, directories, files in os.walk(directory):
        for filename in files:

            file_paths.append(filename)  # Add it to the list.

    return file_paths

def downloadVideo(link, name) :
    mp3file = urllib.urlopen(link)
    with open("data/video/" + name + ".mp4", 'wb') as output:
        output.write(mp3file.read())

def downloadImage(link, name) :
<<<<<<< HEAD
    urllib.urlretrieve(link, "Data/Image/" + name + ".jpg")
=======
    a = 1
    urllib.urlretrieve(link, "data/image/" + name + ".jpg")
>>>>>>> 5300069628d81c512c892f6b69e6d970216ca3d7

def downloadPptx(link, name) :
    urllib.urlretrieve(link, "Data/pptx/" + name + ".odp")

def prepareFile() :
    listVideoFile = get_filepaths('data/video')

    for a in listVideoFile:
        currentDirectory = 'data/video/' + a
        newDirectory  = 'Temp/video/' + a
        shutil.move(currentDirectory, newDirectory)

    listImageFile = get_filepaths('data/image')
    for a in listImageFile:
        currentDirectory = 'data/image/' + a
        newDirectory = 'Temp/image/' + a
        shutil.move(currentDirectory, newDirectory)

    listPptxFile = get_filepaths('Data/pptx')
    for a in listPptxFile :
        currentDirectory = 'Data/pptx/' + a
        newDirectory = 'Temp/pptx/' + a
        shutil.move(currentDirectory, newDirectory)

def downloadData(data) :
    listVideoName = get_filepaths('Temp/video')
    listImageName = get_filepaths('Temp/image')
    for a in data :
        mediaFile = a['mediaFile']
        name = mediaFile['name']
        extension = mediaFile['extension']
        link = mediaFile['link']
        fullname = name + '.' + extension
        if extension == 'jpg' :
            currentDirectory = 'Temp/image/' + fullname
            newDirectory = 'data/image/' + fullname
            if fullname in listImageName :
                shutil.move(currentDirectory, newDirectory)
            else :
                downloadImage(link, name)
<<<<<<< HEAD
        elif extension == 'mp4' :
            currentDirectory = 'Temp/Video/' + fullname
            newDirectory = 'Data/Video/' + fullname
=======
        else :
            currentDirectory = 'Temp/video/' + fullname
            newDirectory = 'data/video/' + fullname
>>>>>>> 5300069628d81c512c892f6b69e6d970216ca3d7
            if fullname in listVideoName:
                shutil.move(currentDirectory, newDirectory)
            else:
                downloadVideo(link, name)
        elif extension == 'odp' :
            currentDirectory = 'Temp/pptx/' + fullname
            newDirectory = 'Data/pptx/' + fullname
            if fullname in listVideoName:
                shutil.move(currentDirectory, newDirectory)
            else:
                downloadPptx(link, name)

def blackScreen():
    pygame.mouse.set_visible(False)
    #screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    #screen.fill((0, 0, 0))
    
 #   for event in pygame.event.get():
  #      if event.type == pygame.QUIT :
   #         pygame.quit()
    #    elif event.type == pygame.KEYDOWN :
     #       if event.key == pygame.K_ESCAPE :
      #          pygame.quit()
    
    
def removeFile():
    shutil.rmtree('Temp/video')
    shutil.rmtree('Temp/image')

def batch() :
   
    url  = "http://128.199.93.67/WiredNoticeboard-Web/api/web/index.php/v1/device/get-device"
    token = rpiSerial.getserial()
    post_data = {'token': token}
    get_response = requests.post(url=url, data=post_data)
    data = json.loads(get_response.text)
    if (get_response.text == '-1') :
        print('This device does not register!')
    else :
        print(data)
        auth = "Bearer " + data['token']
        device_id = data['device_id']
        #print(auth)
        url = "http://128.199.93.67/WiredNoticeboard-Web/api/web/index.php/v1/device-media/get-media"
        headers = {'Authorization': '%s' % auth}
        post_data = {'device_id' : device_id}
        get_response = requests.get(url, data=post_data, headers=headers)
        data = json.loads(get_response.text)
        downloadData(data)
        removeFile()
        for a in data :
            iteration = a['iteration']
            mediaFile = a['mediaFile']
            name = mediaFile['name']
            extension = mediaFile['extension']
            for i in range(0, iteration) :
                if extension == 'jpg':
<<<<<<< HEAD
                    subprocess.call(["fbi", "-noverbose", "-a", "-1", "-T", "2", "-once", "Data/Image/" + name + ".jpg"])
                    time.sleep(3)
                    #subprocess.call(["pkill", "fbi"])
                    #os.system('pkill fbi >/dev/null 2>/dev/null')
                    time.sleep(0.3)
                if extension == 'mp4':
         #           print "1" + name
                    subprocess.call(["omxplayer", "Data/Video/" + name + ".mp4"])
                if extension == 'odp' :
                    subprocess.call(["libreoffice", "--show", "Data/pptx/" + name + ".odp"])
            blackScreen()
=======
                    subprocess.call(["fbi", "-a", "-T", "2", "data/image/" + name + ".jpg"])
                    time.sleep(5)
                    subprocess.call(["pkill", "fbi"])
                else :
                    print "1" + name
                    subprocess.call(["omxplayer", "data/video/" + name + ".mp4"])
>>>>>>> 5300069628d81c512c892f6b69e6d970216ca3d7

if __name__ == "__main__" :
    pygame.init()
    blackScreen()
    for i in range(0, 2) : 
        createFolder()
        prepareFile()
        batch()
    
