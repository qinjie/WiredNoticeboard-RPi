import requests
import json
import urllib
import os
import subprocess
import time
import shutil
import pygame

import rpiSerial
import rpiPdf

def internet_on():
    try:
        requests.urlopen('http://128.199.93.67', timeout=1)
        return True
    except requests.URLError as err:
        return False

def createFolder():
    if not os.path.exists('Data') :
        os.makedirs('Data')
    if not os.path.exists('Data/Video'):
        os.makedirs('Data/Video')
    if not os.path.exists('Data/Image'):
        os.makedirs('Data/Image')
    if not os.path.exists('Data/Pdf') :
        os.makedirs('Data/Pdf')

    if not os.path.exists('Temp') :
        os.makedirs('Temp')
    if not os.path.exists('Temp/Video') :
        os.makedirs('Temp/Video')
    if not os.path.exists('Temp/Image') :
        os.makedirs('Temp/Image')
    if not os.path.exists('Temp/Pdf') :
        os.makedirs('Temp/Pdf')


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

def downloadPdf(link, name) :
    urllib.urlretrieve(link, "Data/Pdf/" + name + ".pdf")

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

    listPptxFile = get_filepaths('Data/Pdf')
    for a in listPptxFile :
        currentDirectory = 'Data/Pdf/' + a
        newDirectory = 'Temp/Pdf/' + a
        shutil.move(currentDirectory, newDirectory)

def downloadData(data) :
    listVideoName = get_filepaths('Temp/Video')
    listImageName = get_filepaths('Temp/image')
    listPdfname = get_filepaths('Temp/pdf')
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
        elif extension == 'mp4' :
            currentDirectory = 'Temp/Video/' + fullname
            newDirectory = 'Data/Video/' + fullname
            if fullname in listVideoName:
                shutil.move(currentDirectory, newDirectory)
            else:
                downloadVideo(link, name)
        elif extension == 'pdf' :
            currentDirectory = 'Temp/Pdf/' + fullname
            newDirectory = 'Data/Pdf/' + fullname
            if fullname in listVideoName:
                shutil.move(currentDirectory, newDirectory)
            else:
                downloadPdf(link, name)

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
    

def showImagePdf() :
    file_list = []
    with open("file_list.txt") as f:
        for line in f:
            file_list.append(line.strip())

    for file_name in file_list :
        subprocess.call(("feh", "-Z", "-F", "-z", "-Y", "-D", "3", "Data/image" + file_name))

def removeFile():
    shutil.rmtree('Temp/Video')
    shutil.rmtree('Temp/Image')

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
                    subprocess.call(( "feh", "-Z", "-F", "-z", "-Y", "-D", "3", "Data/image" + name + ".jpg" ))
                if extension == 'mp4':
         #           print "1" + name
                    subprocess.call(["omxplayer", "Data/Video/" + name + ".mp4"])
                if extension == 'pdf' :
                    rpiPdf.pdfFile()
                    showImagePdf()

            blackScreen()

if __name__ == "__main__" :
    pygame.init()
    blackScreen()
    for i in range(0, 2) : 
        createFolder()
        prepareFile()
        batch()
    
