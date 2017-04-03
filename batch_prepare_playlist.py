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

FOLDER_DOWNLOAD = "download"
FOLDER_IMAGES = "data/image"
FOLDER_VIDEO = "data/video"
CONFIG_FILE = 'device.json'
INI_FILE = 'server.ini'

_path_cur_dir = os.path.dirname(os.path.realpath(__file__))
_file_config = os.path.join(_path_cur_dir, CONFIG_FILE)
_file_ini = os.path.join(_path_cur_dir, INI_FILE)
_path_data_image = os.path.join(_path_cur_dir, FOLDER_IMAGES)
_path_data_video = os.path.join(_path_cur_dir, FOLDER_VIDEO)
_path_download = os.path.join(_path_cur_dir, FOLDER_DOWNLOAD)

def make_folders():
    if not os.path.exists(_path_download):
        os.makedirs(_path_download)
    if not os.path.exists(_path_data_image):
        os.makedirs(_path_data_image)
    if not os.path.exists(_path_data_video):
        os.makedirs(_path_data_video)

def read_ini(ini_file):
    parser = ConfigParser.SafeConfigParser()
    parser.read(ini_file)
    parser.defaults()
    base_url = parser.get('default', 'url_base')
    urls = {}
    urls['device_enroll'] = base_url + parser.get('default','device_enroll')
    urls['device_playlist'] = base_url + parser.get('default','device_playlist')
    urls['device_download'] = base_url + parser.get('default','device_download_file')
    return urls

def download_file_with_token(url, headers, filename='temp'):
    r = requests.get(url, headers=headers, stream=True)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
        return filename
    else:
        return None



# Create folders
make_folders()

# Read server.ini file
urls=[]
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

# Get media list
print 'Fetch media list'
file_list = []
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
headers['Token'] = config_json['token']
r = requests.get(urls['device_playlist'], headers=headers)
js = r.json()
with open('file_list.txt', 'wb') as f:
    for j in js:
        f.write(j['file_path'] + '\n')
        file_list.append(j['file_path'])

# Download media files
print 'Download media files'
for j in js:
    file_path = os.path.join(_path_download, j['file_path'])
    print file_path
    if not os.path.exists(file_path):
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        headers['Token'] = config_json['token']
        url = urls['device_download'].replace('{file}', j['file_path'])
        print url
        download_file_with_token(url, headers, file_path)

def clean_output_folder():
    ## Clean output image folder
    if not os.path.exists(_path_data_image):
        os.makedirs(_path_data_image)
    else:
        flist = os.listdir(_path_data_image)
        for f in flist:
            os.remove(os.path.join(_path_data_image, f))

    ## Clean output video folder
    if not os.path.exists(_path_data_video):
        os.makedirs(_path_data_video)
    else:
        flist = os.listdir(_path_data_video)
        for f in flist:
            os.remove(os.path.join(_path_data_video, f))


clean_output_folder()

# Process input files into output folder
#   copy image and export pdf
for index, file_name in enumerate(file_list):
    new_file_name = "{0:04}_{1}".format(index, file_name)
    print new_file_name
    # Export PDF into images
    input_file = os.path.join(_path_cur_dir, FOLDER_DOWNLOAD, file_name)

    if input_file.endswith('.pdf'):
        # Export PDF to images
        input_file2 = os.path.join(_path_cur_dir, FOLDER_DOWNLOAD, new_file_name)
        print input_file2
        shutil.copy2(input_file, input_file2)
        utilsWand.pdf_to_png(input_file_path=input_file2, output_dir_path=_path_data_image)
        os.remove(input_file2)
    elif utilsOther.get_image_type(input_file):
        # Copy image to data/image folder
        output_file = os.path.join(_path_data_image, new_file_name)
        print output_file
        shutil.copy2(input_file, output_file)
    elif utilsOther.get_video_type(input_file):
        # Copy image to data/video folder
        output_file = os.path.join(_path_data_video, new_file_name)
        print output_file
        shutil.copy2(input_file, output_file)

# Run FEH with following parameters
    # -Y (hide pointer) -x (borderless window) -q (quiet no error reporting)
    # -D 2 (delay 2 sec) -R 10 (reload in 10 sec) -S filename (sort by filename)
    # -B black (black background) -F (fullscreen) -Z (auto zoom) -r (recursive)

# feh -Y -x -q -D 2 -R 10 -S filename -B black -F -Z -r ./data/image
