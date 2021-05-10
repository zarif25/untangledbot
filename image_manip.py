import math
import textwrap
from PIL import Image, ImageFont, ImageDraw


class Font:
    bold = ImageFont.truetype("GilroyBold.ttf", 95)
    regular = ImageFont.truetype("GilroyRegular.ttf", 40)
    black = ImageFont.truetype("GilroyBlack.ttf", 50)
    medium = ImageFont.truetype("GilroyMedium.ttf", 44)


def resize_cover(img, width=1800, height=1000):
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


def create_template(title, sub_title, src, date, img, theme):
    # theme selection
    template, fg_primary = {
        'dark':  (Image.open('untangled_post_template_dark.png'), '#efefef'),
        'light': (Image.open('untangled_post_template_light.png'), '#191919')
    }[theme]

    # extracting from stories

    # formatting
    img = resize_cover(Image.open(img))
    title_wraped = textwrap.wrap(title, width=38)
    sub_title_wraped = textwrap.wrap(sub_title, width=48)

    # image
    template.paste(img, (100, 870))

    # spacing
    height_for_next_element = 100
    spacing_factor = 0
    if len(title_wraped) <= 2:
        if len(sub_title_wraped) <= 5:
            spacing_factor = 30
        elif len(sub_title_wraped) <= 6:
            spacing_factor = 25

    # ready to draw
    draw = ImageDraw.Draw(template)

    # title
    for str in title_wraped:
        draw.text(
            (100, height_for_next_element),
            str,
            fill=fg_primary,
            font=Font.bold
        )
        height_for_next_element += 100
    height_for_next_element += 30 + spacing_factor

    # date
    draw.text(
        (100, height_for_next_element),
        date,
        fill=fg_primary,
        font=Font.regular
    )
    height_for_next_element += 50

    # source
    draw.text(
        (100, height_for_next_element),
        f'Source: {src}',
        fill=fg_primary,
        font=Font.black
    )
    height_for_next_element += 80 + spacing_factor

    # sub title
    rect_width = 15
    rect_height = len(sub_title_wraped)*50
    rect_shape = [
        (100, height_for_next_element),
        (rect_width+100, rect_height+height_for_next_element)
    ]
    height_for_next_element += 5
    draw.rectangle(rect_shape, fill="#868686")
    for str in sub_title_wraped:
        draw.text(
            (130, height_for_next_element),
            str,
            fill=fg_primary,
            font=Font.medium
        )
        height_for_next_element += 50

    return template
