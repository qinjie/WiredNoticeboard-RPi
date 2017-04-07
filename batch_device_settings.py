import os
import utilsWand
import utilsOther
import shutil
import json
import ConfigParser
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

CONFIG_FILE = 'device.json'
INI_FILE = 'server.ini'

_path_cur_dir = os.path.dirname(os.path.realpath(__file__))
_file_config = os.path.join(_path_cur_dir, CONFIG_FILE)
_file_ini = os.path.join(_path_cur_dir, INI_FILE)


def read_ini(ini_file):
    parser = ConfigParser.SafeConfigParser()
    parser.read(ini_file)
    parser.defaults()
    base_url = parser.get('default', 'url_base')
    urls = {}
    urls['device_enroll'] = base_url + parser.get('default', 'device_enroll')
    urls['device_playlist'] = base_url + parser.get('default', 'device_playlist')
    urls['device_profile'] = base_url + parser.get('default', 'device_profile')
    urls['device_download'] = base_url + parser.get('default', 'device_download_file')
    return urls


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


# Read server.ini file
urls = []
if not os.path.exists(INI_FILE):
    print 'Missing server ini file.'
    exit(1)
else:
    urls = read_ini(ini_file=_file_ini)
    print "URL Config: {}".format(urls)

# Read device.json file
config_json = {}
if not os.path.exists(CONFIG_FILE):
    print 'Missing device configuration file.'
    exit(1)
else:
    with open(_file_config, 'rb') as f:
        str = f.read()
        config_json = json.loads(str)
    if 'mac' not in config_json:
        print 'Missing device mac ID in configuration file.'
        exit(1)

# Get token if not available
if 'token' not in config_json:
    if 'mac' in config_json:
        print config_json['mac']
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        headers['Mac'] = config_json['mac']
        r = requests.post(urls['device_enroll'], headers=headers)
        print "URL: {}".format(urls['device_enroll'])
        print "Header = {} {}".format(r.status_code, r.headers['content-type'])
        print "Content = {}".format(r.text)
        if r.status_code == 200:
            j = json.loads(r.text)
            config_json.update(j)
            print "New Config: {}".format(config_json)
            with open(_file_config, 'w') as f:
                f.write(json.dumps(config_json))

    if 'token' not in config_json:
        print 'No device token available'
        exit(1)
# Download device settings
else:
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    headers['Token'] = config_json['token']
    url = urls['device_profile']
    r = requests.get(url, headers=headers, stream=True)
    if r.status_code == 200:
        j = json.loads(r.text)
        config_json.update(j)
        print "New Config: {}".format(config_json)
        with open(_file_config, 'w') as f:
            f.write(json.dumps(config_json))
