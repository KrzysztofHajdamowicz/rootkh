#!/home/krzyszt/.virtualenvs/rootkh/bin/python
#!/usr/bin/env python

import argparse
import configparser
import os
import random
import string

from tinydav import HTTPClient
from PIL import Image, ImageOps

try:
    from io import BytesIO
except ImportError:
    import StrinIO as BytesIO


HOME = os.path.expanduser("~")
config = configparser.ConfigParser()
# config.read(os.path.join(HOME, '.roothkrc'))
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

argparser = argparse.ArgumentParser()
argparser.add_argument("--method", "-m", help="Select method for upload")
argparser.add_argument("--width", "-W", help="")
argparser.add_argument("--height", "-H", help="")
argparser.add_argument("files", help="Select method for upload", nargs="+")
args = argparser.parse_args()


def random_name():
    return ''.join(random.sample(string.ascii_letters * 3 + string.digits * 5, 10))


def minify(file):
    image = Image.open(file)
    width = args.width or config.getint('default', 'width')
    height = args.height

    if width and height:
        thumb = ImageOps.fit(image, (width, height), Image.ANTIALIAS)
    elif width:
        thumb = image.copy()
        thumb.thumbnail((width, width))
    else:
        raise ValueError("WTF?")

    return image, thumb



def upload_webdav(filepath):
    client = HTTPClient(host=config['webdav']['host'],
                        port=config.getint('webdav', 'port'))
    image_uri, thumb_uri = random_name(), random_name()
    image, thumb = minify(filepath)

    def save(img, img_uri):
        with BytesIO() as byte_file:
            img.save(byte_file, format='jpeg')
            byte_file.seek(0)
            client.put(img_uri, byte_file.read())

    save(image, image_uri)
    save(thumb, thumb_uri)

def upload(file):
    upload_method = args.method or config['default']['method']


if __name__ == "__main__":
    upload_webdav('/home/krzyszt/Pictures/syaoran_de_tsubasa_clamp_by_tsubasashaoran.jpg')
    print(config.getboolean('default', 'bbcode'))
    print(args)
