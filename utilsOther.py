import os
import string

import requests


def get_image_type(file_path):
    image_types = {'.jpg':'JPG', '.png':'PNG'}
    name, ext = os.path.splitext(file_path)
    return image_types.get(ext.lower())

def get_video_type(file_path):
    image_types = {'.mp4':'MP4'}
    name, ext = os.path.splitext(file_path)
    return image_types.get(ext.lower())

def web_site_online(url='http://www.google.com/', timeout=5):
    try:
        req = requests.get(url, timeout=timeout)
        # HTTP errors are not raised by default, this statement does that
        req.raise_for_status()
        return True
    except requests.HTTPError as e:
        print("Checking internet connection failed, status code {0}.".format(
        e.response.status_code))
    except requests.ConnectionError:
        print("No internet connection available.")
    return False