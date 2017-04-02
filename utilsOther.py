import os
import string

def get_image_type(file_path):
    image_types = {'.jpg':'JPG', '.png':'PNG'}
    name, ext = os.path.splitext(file_path)
    return image_types.get(ext.lower())

def get_video_type(file_path):
    image_types = {'.mp4':'MP4'}
    name, ext = os.path.splitext(file_path)
    return image_types.get(ext.lower())

