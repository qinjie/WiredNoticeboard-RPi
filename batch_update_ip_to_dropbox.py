import os
import dropbox
import re
import utilsRpi

# create file
hostname = utilsRpi.get_hostname()
filename = utilsRpi.format_filename(hostname) + '.txt'
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
d = dropbox.Dropbox('sTelSxtdJdIAAAAAAAJIX6Jcqwq6XhoSUTR43OmNxPd0LvYceJJWoMCPXM-AIsfq')
target_file = '/ip/' + filename

# open the file and upload it
with open(source_file, "rb") as f:
    # upload gives you metadata about the file
    # we want to overwite any previous version of the file
    meta = d.files_upload(f.read(), target_file, mode=dropbox.files.WriteMode("overwrite"))

