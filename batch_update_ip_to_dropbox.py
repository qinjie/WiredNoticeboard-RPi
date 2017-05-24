import os

import dropbox
import time

import utilsOther
import utilsRpi

DROPBOX_APP_SECRET = 'sTelSxtdJdIAAAAAAAJIX6Jcqwq6XhoSUTR43OmNxPd0LvYceJJWoMCPXM-AIsfq'

# Wait for internet connection
WAIT_ONLINE_SECONDS = 300  # Wait for 5 minutes
count = 0
while not utilsOther.web_site_online():
    if count >= WAIT_ONLINE_SECONDS:
        exit(2)
    print "Wait for internet connection."
    time.sleep(15)  # Delay for 15 seconds
    count = count + 15

# create file
hostname = utilsRpi.get_hostname()
serial = utilsRpi.getserial()
filename = utilsRpi.format_filename(serial+"_"+hostname) + '.txt'
folder = os.path.dirname(os.path.realpath(__file__))
source_file = os.path.join(folder, filename)
with open(source_file, 'wb') as f:
    ip = utilsRpi.get_ip_address('wlan0')
    if ip:
        f.write("wlan0 = {}\n".format(ip))
    ip = utilsRpi.get_ip_address('eth0')
    if ip:
        f.write("eth0 = {}\n".format(ip))

# Create a dropbox object using an API v2 key
# Pointing to dropbox RaspberryPiMonitor folder
d = dropbox.Dropbox(DROPBOX_APP_SECRET)
target_file = '/ip/' + filename

# open the file and upload it
with open(source_file, "rb") as f:
    # upload gives you metadata about the file
    # we want to overwite any previous version of the file
    meta = d.files_upload(f.read(), target_file, mode=dropbox.files.WriteMode("overwrite"))
