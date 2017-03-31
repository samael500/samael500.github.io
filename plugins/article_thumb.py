import os
import re
import logging
logger = logging.getLogger(__name__)

from pelican import signals
from pelican.contents import Content, Article

try:
    from PIL import Image, ImageOps
    enabled = True
except ImportError:
    logging.warning("Unable to load PIL, disabling thumbnailer")
    enabled = False


images = []

def thumb_path(img):
    """ make thumb suffix """
    path, ext = os.path.splitext(img)
    return '{}.thumb{}'.format(path, ext)


def scale(width, height, res_width):
    res_height = int(float(height) * res_width / width)
    return res_width, res_height


def add_thumb(content):
    if not isinstance(content, Article) or not hasattr(content, 'image'):
        return

    src = os.path.abspath(content.settings['PATH'] + content.image)
    if not os.path.exists(src):
        return

    if not hasattr(content, 'thumb'):
        content.thumb = thumb_path(content.image)
        images.append(content.image)

    with Image.open(src) as img:
        content.image_width, content.image_height = img.size


def make_thumbnails(pelican):
    logger.debug("Thumbnailer Started")
    for img_path in images:
        src = os.path.abspath(pelican.settings['OUTPUT_PATH'] + img_path)
        dest = thumb_path(src)
        logger.debug('Save image\nfrom: {}\n  to: {}'.format(src, dest))
        with Image.open(src) as image:
            thumb = ImageOps.fit(image, scale(*image.size, res_width=699), Image.ANTIALIAS)
        thumb.save(dest)


def register():
    global enabled
    if not enabled:
        return
    signals.content_object_init.connect(add_thumb)
    signals.finalized.connect(make_thumbnails)
