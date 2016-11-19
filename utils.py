"""
General utils to resize images and create the appication icon
"""
import os
from PIL import Image
from settings import ASSETS_DIR, AUDIO_DIR, ASSETS_DIR, IMGS_DIR

cwd = os.getcwd()

def image_resize(img_path, size):
    image = Image.open(img_path)
    resized = image.resize(size=size)
    #resized.show()
    return resized

def make_app_icon(img_path, newname='app_icon.png'):
    image = image_resize(img_path, (32, 32))
    newpath = os.path.join(IMGS_DIR, newname)
    image.save(fp=newpath)


if __name__ == "__main__":
    make_app_icon(os.path.join(IMGS_DIR, "racecar.png"))