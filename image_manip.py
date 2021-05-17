import math
import textwrap
from PIL import Image, ImageFont, ImageDraw


class Font:
    black = ImageFont.truetype("00_GilroyBlack.ttf", 45)
    bold = ImageFont.truetype("00_GilroyBold.ttf", 95)
    medium = ImageFont.truetype("00_GilroyMedium.ttf", 44)
    medium_large = ImageFont.truetype("00_GilroyMedium.ttf", 50)
    regular = ImageFont.truetype("00_GilroyRegular.ttf", 40)


def resize_cover(img, is_content_short):
    width = 1800
    height = 1050 if is_content_short else 1000
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
    verify(title, description, src, date, img, theme)

    # set is_text_only
    is_text_only = img == None

    # formatting
    title_wrapped = textwrap.wrap(title, width=37)
    description_wrapped = get_description_wrapped(
        description, is_text_only, title_wrapped)

    # spacing
    spacing_factor = get_spacing_factor(
        title_wrapped, description_wrapped, is_text_only)

    # set is_content_short
    is_content_short = spacing_factor > 250 and not is_text_only

    # re-wrap description with new font-size
    if is_content_short:
        description = ' '.join(description_wrapped)
        description_wrapped = textwrap.wrap(description, width=45)

    # theme selection
    template = get_template(is_content_short, is_text_only, theme)
    fg_color = get_fg_color(theme)

    # image
    if not is_text_only:
        put_image(template, img, is_content_short)

    if spacing_factor < 0:
        spacing_factor = 0
    elif spacing_factor > 100:
        spacing_factor = 100

    # ready to draw
    draw = ImageDraw.Draw(template)

    # source
    put_source(draw, src, fg_color)

    height_for_next_element = get_height_for_next_element(
        is_text_only, is_content_short)

    # title
    height_for_next_element = put_title(
        title_wrapped, spacing_factor, fg_color, draw, height_for_next_element)

    # date
    height_for_next_element = put_date(
        date, spacing_factor, fg_color, draw, height_for_next_element)

    # description
    put_description(description_wrapped, is_content_short,
                    fg_color, draw, height_for_next_element)

    return template


def put_title(title_wrapped, spacing_factor, fg_color, draw, height_for_next_element):
    for str in title_wrapped:
        draw.text(
            (100, height_for_next_element),
            str,
            fill=fg_color,
            font=Font.bold
        )
        height_for_next_element += 100
    height_for_next_element += spacing_factor/3
    return height_for_next_element


def put_description(description_wrapped, is_content_short, fg_color, draw, height_for_next_element):
    if description_wrapped[-1][-1] != '.':
        description_wrapped[-1] += '.'
    if is_content_short:
        line_height = 70
        space_left = 150
        space_top = 10
        font = Font.medium_large
    else:
        line_height = 50
        space_left = 140
        space_top = 5
        font = Font.medium
    description_height = len(description_wrapped)*line_height
    rect_width = 15
    rect_height = description_height
    rect_shape = [
        (100, height_for_next_element),
        (rect_width+100, rect_height+height_for_next_element)
    ]
    height_for_next_element += space_top
    draw.rectangle(rect_shape, fill="#868686")
    for str in description_wrapped:
        draw.text(
            (space_left, height_for_next_element),
            str,
            fill=fg_color,
            font=font
        )
        height_for_next_element += line_height


def put_date(date, spacing_factor, fg_color, draw, height_for_next_element):
    draw.text(
        (100, height_for_next_element),
        date,
        fill=fg_color,
        font=Font.regular
    )
    height_for_next_element += 70 + spacing_factor/2
    return height_for_next_element


def verify(title, description, src, date, img, theme):
    """throws exception if arguments are invalid"""
    if None in [title, description, src, date] or theme not in ['light', 'dark']:
        raise Exception("Invalid arguements")


def get_height_for_next_element(is_text_only, is_content_short):
    if is_text_only:
        return 1050
    if is_content_short:
        return 1200
    return 100


def get_fg_color(theme):
    return '#efefef' if theme == 'dark' else '#191919'


def get_template(is_content_short, is_text_only, theme):
    if is_text_only:
        return {
            'dark':  Image.open('00_template_text_only_dark.png'),
            'light': Image.open('00_template_text_only_light.png')
        }[theme]
    if is_content_short:
        return {
            'dark':  Image.open('00_template_content_short_dark.png'),
            'light': Image.open('00_template_content_short_light.png')
        }[theme]
    return {
        'dark':  Image.open('00_template_dark.png'),
        'light': Image.open('00_template_light.png')
    }[theme]


def get_spacing_factor(title_wrapped, description_wrapped, is_text_only):
    if is_text_only:
        writtable_height = 850
    else:
        writtable_height = 720

    title_height = len(title_wrapped)*100
    date_height = 70
    description_height = len(description_wrapped)*50

    return writtable_height - (
        title_height +
        date_height +
        description_height
    )


def get_description_wrapped(description, is_text_only, title_wrapped):
    if is_text_only:
        description_max_char = 81
        description_max_lines = 15 - 2*len(title_wrapped)
    else:
        description_max_char = 50
        description_max_lines = 13 - 2*len(title_wrapped)
    description_wrapped = textwrap.wrap(
        description,
        width=description_max_char
    )
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
    return description_wrapped


def put_source(draw, src, fill):
    if len(src) > 50:
        src.split(",")[-1].strip()
    draw.text(
        (100, 1910),
        f'Source: {src}',
        fill=fill,
        font=Font.black
    )


def put_image(template, img, is_content_short):
    img = resize_cover(Image.open(img), is_content_short)
    if (is_content_short):
        template.paste(img, (100, 100))
    else:
        template.paste(img, (100, 870))
