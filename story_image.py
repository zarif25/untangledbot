import logging
import math
from time import localtime

from PIL import Image, ImageDraw, ImageFont


class Font:
    title = ImageFont.truetype("00_GilroyBold.ttf", 95)
    details = ImageFont.truetype("00_GilroyMedium.ttf", 52)
    src = ImageFont.truetype("00_GilroyBlack.ttf", 45)
    date = ImageFont.truetype("00_GilroyRegular.ttf", 40)


class Spacing:
    title = 20
    details = 20
    date = 10


def wrap_text(text: str, font: ImageFont, width: int) -> list:
    # FIXME: think of a better algorithm
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
    return result


class StoryImage:
    EDITABLE_WIDTH: int = 1800  # width of image - right and left margin

    def __init__(self, story):
        self.__story = story
        self.__img = self.__get_img()

    def save_as(self, img_name):
        if self.__story.is_complete():
            self.__img.save(img_name)
            return img_name
        else:
            raise Exception("Cannot create image from incomplete story")

    def __get_img(self):
        logging.info(f"Creating image for {self.__story}")
        self.__theme = StoryImage.__get_theme()
        self.__is_text_only = self.__story.img == None

        self.__title = self.__get_title()
        self.__date = self.__get_date()
        self.__details = self.__get_details()
        self.__src = self.__get_src()

        self.__is_content_short = self.__get_is_content_short()
        self.__template = self.__get_template()
        self.__fg_color = self.__get_fg_color()

        self.__put_image()
        self.__draw = ImageDraw.Draw(self.__template)
        self.__put_src()
        self.__height_for_next_element = self.__get_initial_height_for_next_element()
        self.__put_title()
        self.__put_date()
        self.__put_details()
        return self.__template

    @staticmethod
    def __get_theme():
        t_hour = (localtime().tm_hour + 6) % 24
        return 'light' if 3 <= t_hour <= 18 else 'dark'

    def __get_title(self):
        return wrap_text(self.__story.title, Font.title, self.EDITABLE_WIDTH)

    def __get_date(self) -> str:
        return self.__story.datetime.strftime("%A, %b %d, %Y")

    def __get_details(self):
        # wrap details
        left_rect_and_margin = 50
        right_rect_and_margin = 0 if self.__is_text_only else 650
        max_width = self.EDITABLE_WIDTH - right_rect_and_margin - left_rect_and_margin
        details = wrap_text(self.__story.details, Font.details, max_width)

        # trim details
        if self.__is_text_only:
            max_lines = 13 - 2*len(self.__title)
        else:
            max_lines = 11 - 2*len(self.__title)

        if len(details) > max_lines:
            details_trimmed = details[:max_lines]
            i = max_lines-1
            while i >= 0:
                fullstop = details_trimmed[i].find('.')
                quesmark = details_trimmed[i].find('?')
                exclammark = details_trimmed[i].find('!')
                if fullstop != -1:
                    details_trimmed[i] = details_trimmed[i][:fullstop+1]
                    break
                elif quesmark != -1:
                    details_trimmed[i] = details_trimmed[i][:quesmark+1]
                    break
                elif exclammark != -1:
                    details_trimmed[i] = details_trimmed[i][:exclammark+1]
                    break
                else:
                    del details_trimmed[i]
                i -= 1
            if details_trimmed:
                details = details_trimmed
            else:
                details = details[:max_lines]
                details[-1] = ' '.join(details[-1].split(' ')[:-1])+"..."
        return details

    def __get_src(self) -> str:
        src = self.__story.src
        if Font.src.getlength(src) > 1200:
            src = self.__story.src.split(",")[-1].strip()
        return src

    def __get_is_content_short(self):
        '''
        height of title font is roughly twice the height of details font
        so, title*2 + details is a good approximation of content height
        true if the content height if less than 10 detail-font-height-units and
        title is less than 3 lines
        '''
        title_height = len(self.__title)
        details_height = len(self.__details)
        return not self.__is_text_only and title_height < 3 and title_height*2 + details_height < 10

    def __get_fg_color(self):
        return '#efefef' if self.__theme == 'dark' else '#191919'

    def __get_template(self):
        if self.__is_text_only:
            type = '_text_only'
        elif self.__is_content_short:
            type = '_content_short'
        else:
            type = ''
        return Image.open(f'00_template{type}_{self.__theme}.png')

    def __get_initial_height_for_next_element(self):
        if self.__is_text_only:
            return 1050
        if self.__is_content_short:
            return 1240
        return 100

    def __put_image(self):
        if not self.__is_text_only:
            img = self.__get_resized_image()
            if (self.__is_content_short):
                self.__template.paste(img, (100, 100))
            else:
                self.__template.paste(img, (100, 870))

    def __get_resized_image(self):
        width = self.EDITABLE_WIDTH
        height = 1100 if self.__is_content_short else 1000
        img = Image.open(self.__story.img)

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

    def __put_src(self):
        self.__draw.text(
            (100, 1910),
            f'Source: {self.__src}',
            fill=self.__fg_color,
            font=Font.src
        )

    def __put_title(self):
        self.__put_text(
            self.__title,
            Font.title,
            Spacing.title,
        )

    def __put_date(self):
        self.__put_text(
            [self.__date],
            Font.date,
            Spacing.date,
        )

    def __put_details(self):
        self.__put_text(
            self.__details,
            Font.details,
            Spacing.details,
            has_left_border=True
        )

    def __put_text(self, text: list[str], font: ImageFont, spacing: int, has_left_border=False, left_margin: int = 100):
        text = '\n'.join(text)

        content_height = font.getsize_multiline(
            text,
            spacing=spacing
        )[1] + spacing

        if has_left_border:
            border_width = 15
            padding_top = 10
            rect_shape = [
                (left_margin, self.__height_for_next_element),
                (border_width + left_margin,
                 content_height + padding_top + self.__height_for_next_element)
            ]
            self.__height_for_next_element += padding_top
            self.__draw.rectangle(rect_shape, fill="#868686")
            left_margin += 40

        self.__draw.multiline_text(
            (left_margin, self.__height_for_next_element),
            text,
            spacing=spacing,
            fill=self.__fg_color,
            font=font
        )
        self.__height_for_next_element += content_height + 30
