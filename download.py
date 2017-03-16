import urllib.request

# urllib.request.urlretrieve("http://128.199.93.67/WiredNoticeboard-Web/frontend/web/uploads/2_58c0aa25d1f82.mp4", "a.mp4")
mp3file = urllib.request .urlopen("http://128.199.93.67/WiredNoticeboard-Web/frontend/web/uploads/2_58c0aa25d1f82.mp4")
with open('b.mp4','wb') as output:
    output.write(mp3file.read())
