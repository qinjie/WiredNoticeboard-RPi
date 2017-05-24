import ConfigParser
import json
import os

import requests

####
# This script is the main script to download slideshow files from server
# 1. Get file list in play order into file_list.txt
# 2. Download files into "download" folders
# 3. For each file in file_list with index i
# 	Get file from download folder
# 	If it's a image file, copy to "pictures" folder and rename it as "<i>_<filename>"
# 	If it's a pdf file, export it as images to "pictures" foder with name "<i>_<filename>_<page>"
# 4. Run Feh with slide show
# 5. Play video files
####

INI_FILE = 'device.ini'
CONFIG_FILE = 'device.json'

_path_cur_dir = os.path.dirname(os.path.realpath(__file__))
_file_config = os.path.join(_path_cur_dir, CONFIG_FILE)
_file_ini = os.path.join(_path_cur_dir, INI_FILE)


def read_ini_file(ini_file):
    parser = ConfigParser.SafeConfigParser()
    parser.read(ini_file)
    parser.defaults()
    settings = {}
    base_url = parser.get('server', 'url_base')
    settings['device_enroll'] = base_url + parser.get('server', 'device_enroll')
    settings['device_playlist'] = base_url + parser.get('server', 'device_playlist')
    settings['device_profile'] = base_url + parser.get('server', 'device_profile')
    settings['device_download'] = base_url + parser.get('server', 'device_download_file')
    # Get device values
    settings['device_mac'] = parser.get('device', 'device_mac')
    settings['device_label'] = parser.get('device', 'device_label')

    return settings

def read_config(filepath):
    if not os.path.exists(filepath):
        print 'Missing device configuration file.'
        return {}
    else:
        with open(filepath, 'rb') as f:
            str = f.read()
            return json.loads(str)


def download_file_with_token(url, headers, filename='temp'):
    r = requests.get(url, headers=headers, stream=True)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
        return filename
    else:
        return None


# Read ini file
settings = []
if not os.path.exists(_file_ini):
    print 'Missing device ini file.'
    exit(1)
else:
    settings = read_ini_file(ini_file=_file_ini)
    print "Settings: {}".format(settings)

if not settings['device_mac']:
    print 'Missing device mac ID in file {}.'.format(INI_FILE)
    exit(1)

# Read device.json file
config_json = read_config(_file_config)

# Get token if not available
if 'token' not in config_json:
    if settings['device_mac']:
        print settings['device_mac']
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        headers['Mac'] = settings['device_mac']
        r = requests.post(settings['device_enroll'], headers=headers)
        print "URL: {}".format(settings['device_enroll'])
        print "Header = {} {}".format(r.status_code, r.headers['content-type'])
        print "Content = {}".format(r.text)
        if r.status_code == 200:
            j = json.loads(r.text)
            config_json.update(j)
            print "New Config: {}".format(config_json)
            with open(_file_config, 'w') as f:
                f.write(json.dumps(config_json))
    else:
        print 'Missing device mac ID in file {}.'.format(INI_FILE)
        exit(1)

if 'token' not in config_json:
    print 'No device token available'
    exit(1)

# Download device settings
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
headers['Token'] = config_json['token']
url = settings['device_profile']
r = requests.get(url, headers=headers, stream=True)
if r.status_code == 200:
    j = json.loads(r.text)
    config_json.update(j)
    print "New Config: {}".format(config_json)
    with open(_file_config, 'w') as f:
        f.write(json.dumps(config_json))
