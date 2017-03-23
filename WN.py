import requests
import json
import urllib
import os
import subprocess
import time
import shutil
import pygame



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
    urllib.urlretrieve(link, "Data/Image/" + name + ".jpg")

def downloadPptx(link, name) :
    urllib.urlretrieve(link, "Data/pptx/" + name + ".pptx")

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

    listPptxFile = get_filepaths('Data/pptx')
    for a in listPptxFile :
        currentDirectory = 'Data/pptx/' + a
        newDirectory = 'Temp/pptx/' + a
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
        elif extension == 'mp4' :
            currentDirectory = 'Temp/Video/' + fullname
            newDirectory = 'Data/Video/' + fullname
            if fullname in listVideoName:
                shutil.move(currentDirectory, newDirectory)
            else:
                downloadVideo(link, name)
        elif extension == 'pptx' :
            currentDirectory = 'Temp/pptx/' + fullname
            newDirectory = 'Data/pptx/' + fullname
            if fullname in listVideoName:
                shutil.move(currentDirectory, newDirectory)
            else:
                downloadVideo(link, name)

def blackScreen():
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.flip()
    screen.fill((0, 0, 0))
 #   for event in pygame.event.get():
  #      if event.type == pygame.QUIT :
   #         pygame.quit()
    #    elif event.type == pygame.KEYDOWN :
     #       if event.key == pygame.K_ESCAPE :
      #          pygame.quit()
    
    
def removeFile():
    shutil.rmtree('Temp/Video')
    shutil.rmtree('Temp/Image')

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
                    subprocess.call(["fbi", "-noverbose", "-a", "-1", "-T", "2", "-once", "Data/Image/" + name + ".jpg"])
                    time.sleep(3)
                    #subprocess.call(["pkill", "fbi"])
                    #os.system('pkill fbi >/dev/null 2>/dev/null')
                    time.sleep(0.3)
                else :
         #           print "1" + name
                    subprocess.call(["omxplayer", "Data/Video/" + name + ".mp4"])
            blackScreen()

if __name__ == "__main__" :
    pygame.init()
    blackScreen()
    for i in range(0, 2) : 
        createFolder()
        prepareFile()
        batch()
    
