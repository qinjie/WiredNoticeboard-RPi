import glob
import json
import os


####
# This script runs FEH to slide show images, followed by video play using omxplayer.
# The script can be interrupted by key press CTRL+C multiple times
####
import time


def read_config(filepath):
    if not os.path.exists(filepath):
        print 'Missing device configuration file.'
        return {}
    else:
        with open(filepath, 'rb') as f:
            str = f.read()
            return json.loads(str)


FOLDER_IMAGES = "data/image"
FOLDER_VIDEO = "data/video"
CONFIG_FILE = 'device.json'

_path_cur_dir = os.path.dirname(os.path.realpath(__file__))
_file_config = os.path.join(_path_cur_dir, CONFIG_FILE)
_path_cur_dir = os.path.dirname(os.path.realpath(__file__))
_path_data_image = os.path.join(_path_cur_dir, FOLDER_IMAGES)
_path_data_video = os.path.join(_path_cur_dir, FOLDER_VIDEO)

# Set flag to indicate download completed or not
_download_completed_flag = os.path.join(_path_cur_dir, 'flag_1')
_download_inprogress_flag = os.path.join(_path_cur_dir, 'flag_0')
_download_failed_flag = os.path.join(_path_cur_dir, 'flag_2')

DELAY = 5  # seconds
RELOAD = 10  # seconds

config_json = read_config(_file_config)
slide_timing_second = DELAY
if config_json['slide_timing']:
    slide_timing_second = config_json['slide_timing']

try:
    print "Wait for download to complete."
    while os.path.exists(_download_inprogress_flag):
        time.sleep(15)  # Delay for x seconds

    videos = glob.glob(_path_data_video + '/*')
    if not videos:
        cmd = 'DISPLAY=:0.0 feh -Y -q -F -Z -D {} -R {} -S filename -B black -r {}'.format(
            slide_timing_second, RELOAD, _path_data_image)
        # Play image files
        os.system(cmd + ' > /dev/null')
    else:
        cmd = 'DISPLAY=:0.0 feh -Y -q -F -Z -D {} -R {} -S filename -B black --cycle-once -r {}'.format(
            slide_timing_second, RELOAD, _path_data_image)
        while True:
            # Play image files
            os.system(cmd + ' > /dev/null')
            # Play video files
            for v in videos:
                print "Playing video {}".format(v)
                cmd = 'DISPLAY=:0.0 omxplayer -o hdmi -b {}'.format(v)
                os.system(cmd + ' > /dev/null')

except KeyboardInterrupt:
    exit(2)
