import os
import time
import glob
import subprocess

####
# This script runs FEH to slide show images, followed by video play using omxplayer.
# The script can be interrupted by key press CTRL+C multiple times
####

FOLDER_IMAGES = "data/image"
FOLDER_VIDEO = "data/video"

_path_cur_dir = os.path.dirname(os.path.realpath(__file__))
_path_data_image = os.path.join(_path_cur_dir, FOLDER_IMAGES)
_path_data_video = os.path.join(_path_cur_dir, FOLDER_VIDEO)

DELAY = 5  # seconds
RELOAD = 10  # seconds

try:
    while True:
        # Play image files
        os.system(
            'DISPLAY=:0.0 feh -Y -q -F -Z -D {} -R {} -S filename -B black --cycle-once -r {}'.format(DELAY, RELOAD,
                                                                                                      _path_data_image))
        # Play video files
        videos = glob.glob(_path_data_video + '/*')
        for v in videos:
            print "Playing video {}".format(v)
            cmd = 'DISPLAY=:0.0 omxplayer -o hdmi -b {}'.format(v)
            os.system(cmd)

except KeyboardInterrupt:
    exit(2)
