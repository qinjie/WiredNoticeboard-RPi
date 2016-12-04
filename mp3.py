import subprocess

while (1) :
    
    subprocess.call(["omxplayer", "--no-osd", "sample.mp4"])
    subprocess.call(["omxplayer","--no-osd", "4.mp4"])
    
