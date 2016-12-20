import os

def get_image_type(file_path):
    image_types = {'.jpg':'JPG', '.png':'PNG'}
    name, ext = os.path.splitext(file_path)
    return image_types.get(ext.lower())


