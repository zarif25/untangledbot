import math
import textwrap
from PIL import Image, ImageFont, ImageDraw


class Font:
    black = ImageFont.truetype("GilroyBlack.ttf", 45)
    bold = ImageFont.truetype("GilroyBold.ttf", 95)
    medium = ImageFont.truetype("GilroyMedium.ttf", 44)
    regular = ImageFont.truetype("GilroyRegular.ttf", 40)


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


def create_template(title, description, src, date, img, theme):

    if None in [title, description, src, date]:
        return None

    # theme selection
    fg_primary = {
        'dark':  '#efefef',
        'light': '#191919'
    }[theme]
    if img == None:
        template = {
            'dark':  Image.open('untangled_post_template_text_only_dark.png'),
            'light': Image.open('untangled_post_template_text_only_light.png')
        }[theme]
    else:
        template = {
            'dark':  Image.open('untangled_post_template_dark.png'),
            'light': Image.open('untangled_post_template_light.png')
        }[theme]

    # formatting
    title_wrapped = textwrap.wrap(title, width=37)
    if img==None:
        description_max_char = 81
        description_max_lines = 15 - 2*len(title_wrapped)
    else:
        img = resize_cover(Image.open(img))
        description_max_char = 52
        description_max_lines = 13 - 2*len(title_wrapped)
    description_wrapped = textwrap.wrap(description, width=description_max_char)
    if len(description_wrapped) > description_max_lines:
        description_wrapped = description_wrapped[:description_max_lines]
        i = description_max_lines-1
        while i >= 0:
            if '.' in description_wrapped[i]:
                description_wrapped[i] = '.'.join(
                    description_wrapped[i].split('.')[:-1]) + "."
                break
            else:
                del description_wrapped[i]
            i -= 1

    # image
    if img != None:
        template.paste(img, (100, 870))

    # spacing
    if img == None:
        height_for_next_element = 1050
        writtable_height = 850
    else:
        height_for_next_element = 100
        writtable_height = 720

    title_height = len(title_wrapped)*100
    date_height = 70
    description_height = len(description_wrapped)*50

    spacing_factor = writtable_height - (
        title_height +
        date_height +
        description_height
    )

    if spacing_factor < 0: spacing_factor = 0
    elif spacing_factor > 100: spacing_factor = 100

    # ready to draw
    draw = ImageDraw.Draw(template)

    # title
    for str in title_wrapped:
        draw.text(
            (100, height_for_next_element),
            str,
            fill=fg_primary,
            font=Font.bold
        )
        height_for_next_element += 100
    height_for_next_element += spacing_factor/3

    # date
    draw.text(
        (100, height_for_next_element),
        date,
        fill=fg_primary,
        font=Font.regular
    )
    height_for_next_element += 70 + spacing_factor/2

    # description
    rect_width = 15
    rect_height = description_height
    rect_shape = [
        (100, height_for_next_element),
        (rect_width+100, rect_height+height_for_next_element)
    ]
    height_for_next_element += 5
    draw.rectangle(rect_shape, fill="#868686")
    for str in description_wrapped:
        draw.text(
            (130, height_for_next_element),
            str,
            fill=fg_primary,
            font=Font.medium
        )
        height_for_next_element += 50

    height_for_next_element = 1910

    # source
    draw.text(
        (100, height_for_next_element),
        f'Source: {src}',
        fill=fg_primary,
        font=Font.black
    )

    return template
