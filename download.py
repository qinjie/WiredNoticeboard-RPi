import urllib.request
mp3file = urllib.request .urlopen("http://techslides.com/demos/samples/sample.mp4")
with open('sample.mp4','wb') as output:
    output.write(mp3file.read())
