import math
import os
from datetime import datetime

import pytz
from PIL import Image, ImageFont


def resized_image_to_fit(image_path: str, width: int, height: int) -> Image:
    """
    Args:
        image_path: paht to an image file or url
        width: width of output image
        height: height of output image
    Returns:
        Scales and crops image to width x height dimension and returns an Image object
    """
    img = Image.open(image_path)

    # scale
    img_width, img_height = img.size
    multiplier = max(width/img_width, height/img_height)
    img = img.resize((math.ceil(dimen*multiplier) for dimen in img.size))

    # crop
    img_width, img_height = img.size
    top = (img_height-height)//2
    left = (img_width-width)//2
    img = img.crop((left, top, width+left, height+top))

    return img


def get_theme(zone='Asia/Dhaka'):
    """
    Returns:
        Theme based on current time in Dhaka
    """
    tz = pytz.timezone(zone)
    t_hour = datetime.now(tz).hour
    return 'light' if 3 <= t_hour <= 18 else 'dark'


def wrap_text(text: str, font: ImageFont, width: int) -> str:
    """
    Args:
        text: text to wrap
        font: font of the text
        width: max width
    Returns:
        A multiline string that fits in the given width
    """
    text = text.split(" ")
    result = []
    line = ""
    i = 0
    while i < len(text):
        if font.getlength(line+text[i]) <= width:
            line += text[i] + " "
            i += 1
        else:
            result.append(line)
            line = ""
    if line:
        result.append(line)
    return '\n'.join(result)
