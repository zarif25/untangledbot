from datetime import datetime

from storyimage.banglastuff.dateconversion import to_bn_datetime
from storyimage.banglastuff.unicode2bijoy import to_bijoy
from PIL import Image, ImageFont, ImageDraw
from pathlib import Path
from .utils import get_theme, resized_image_to_fit, wrap_text

__STATIC_DIR = Path(__file__).resolve().parent / 'static'
FONT_DIR = __STATIC_DIR / 'fonts'
TEMPLATE_DIR = __STATIC_DIR / 'templates'
LOGO_DIR = __STATIC_DIR / 'logos'


class Gilroy:
    black = str(FONT_DIR / "GilroyBlack.ttf")
    bold = str(FONT_DIR / "GilroyBold.ttf")
    medium = str(FONT_DIR / "GilroyMedium.ttf")
    regular = str(FONT_DIR / "GilroyRegular.ttf")


class SutonnyMJ:
    bold = str(FONT_DIR / "SutonnyMJ Bold.ttf")
    regular = str(FONT_DIR / "SutonnyMJ Regular.ttf")


COLORS = {
    'light': '#efefef',
    'dark': '#191919',
}


class DefaultStyles:
    margin = 100
    image_size = 2000
    writeable_width = image_size - 2*margin

    def __init__(self) -> None:
        self.writeable_height = 785
        self.text_start = self.margin
        self.style = {
            'image': {
                'x': self.margin,
                'y': 870,
                'width': 1800,
                'height': 1000
            },
            'logo': {
                'bn': {
                    'x': self.image_size - self.margin - 346,
                    'y': 1900,
                    'width': 346,
                    'height': 55
                },
                'en': {
                    'x': self.image_size - self.margin - 244,
                    'y': 1900,
                    'width': 244,
                    'height': 57
                },
            },
            'title': {
                'en': {
                    'x': self.margin,
                    'y': 'used space',
                    'width': self.writeable_width,
                    'font': ImageFont.truetype(Gilroy.bold, 95),
                    'spacing': 20,
                },
                'bn': {
                    'x': self.margin,
                    'y': 'used space',
                    'width': self.writeable_width,
                    'font': ImageFont.truetype(SutonnyMJ.bold, 95),
                    'spacing': 20,
                }
            },
            'date': {
                'en': {
                    'x': self.margin,
                    'y': 'used space',
                    'width': self.writeable_width,
                    'font': ImageFont.truetype(Gilroy.regular, 40),
                    'spacing': 0
                },
                'bn': {
                    'x': self.margin,
                    'y': 'used space',
                    'width': self.writeable_width,
                    'font': ImageFont.truetype(SutonnyMJ.regular, 46),
                    'spacing': 0
                },
            },
            'summary': {
                'en': {
                    'x': self.margin,
                    'y': 'used space',
                    'width': self.writeable_width - 50 - 650,
                    'font': ImageFont.truetype(Gilroy.medium, 52),
                    'spacing': 20,
                    'has_left_border': True
                },
                'bn': {
                    'x': self.margin,
                    'y': 'used space',
                    'width': self.writeable_width - 50 - 650,
                    'font': ImageFont.truetype(SutonnyMJ.regular, 56),
                    'spacing': 14,
                    'has_left_border': True
                },

            },
            'source': {
                'en': {
                    'x': self.margin,
                    'y': 1910,
                    'width': self.writeable_width,
                    'font': ImageFont.truetype(Gilroy.black, 45),
                    'spacing': 0,
                },
                'bn': {
                    'x': self.margin,
                    'y': 1900,
                    'width': self.writeable_width,
                    'font': ImageFont.truetype(SutonnyMJ.regular, 60),
                    'spacing': 0,
                },

            },
        }


class RegularStyles(DefaultStyles):
    pass


class ShortContentStyles(DefaultStyles):
    def __init__(self) -> None:
        super().__init__()
        self.order = ('image', 'title', 'date', 'summary')
        self.style['image']['y'] = self.margin
        self.style['image']['height'] = 1100
        self.writeable_height = 650
        self.text_start = self.margin + self.style['image']['height'] + 50


class ImageCreator():
    def __init__(self, title: str, source: str, summary: str, dtime: datetime, image_path: str, lang: str, template_name: str = 'auto') -> None:
        if lang == 'bn':
            title = to_bijoy(title)
            summary = to_bijoy(summary)
            source = to_bijoy('সূত্র: ' + source)
            dtime = to_bijoy(to_bn_datetime(dtime))
        else:
            source = "Source: " + source
            dtime = dtime.strftime("%A, %b %d, %Y")

        theme = get_theme()
        if template_name == 'auto':
            template_name, summary = self.__get_template_name(
                title, summary, dtime, lang)
        self.__template = Image.open(TEMPLATE_DIR/theme/(template_name+'.png'))
        STYLE, self.used_space = {
            'regular': (RegularStyles().style, RegularStyles().text_start),
            'short_content': (ShortContentStyles().style, ShortContentStyles().text_start),
        }[template_name]
        fg_theme = {
            'light': 'dark',
            'dark': 'light'
        }[theme]
        fg = COLORS[fg_theme]

        # image
        self.__put_image(image_path, **STYLE['image'])

        # logo
        logo_file_name = fg_theme + '.png'
        self.__put_image(LOGO_DIR/lang/logo_file_name, **STYLE['logo'][lang])

        self.__draw = ImageDraw.Draw(self.__template)

        # title
        self.__put_text(title, fg, **STYLE['title'][lang])

        # date
        self.__put_text(dtime, fg, **STYLE['date'][lang])

        # summary
        self.__put_text(summary, fg, **STYLE['summary'][lang])

        # source
        self.__put_text(source, fg, **STYLE['source'][lang])

    @classmethod
    def from_story(cls, story, temp_image_path, template_name: str = 'auto'):
        return cls(
            title=story.title,
            source=story.source,
            summary=story.summary,
            dtime=story.dtime,
            image_path=temp_image_path,
            lang=story.lang,
            template_name=template_name
        )

    def __put_image(self, image_path, x, y, width, height):
        img: Image = resized_image_to_fit(image_path, width, height).convert('RGBA')
        self.__template.paste(img, (x, y), img)

    def __put_text(self, text, fg, x, y, width, font: ImageFont, spacing: int = 0, has_left_border=False):
        if y == 'used space':
            y = self.used_space
            update_used_space = True
        else:
            update_used_space = False
        text = wrap_text(text, font, width)
        content_height = font.getsize_multiline(
            text, spacing=spacing)[1] + spacing
        if has_left_border:
            BORDER_WIDTH = 15
            PADDING_TOP = 5
            PADDING_LEFT = 25
            rect_shape = [
                (x, y),
                (x + BORDER_WIDTH,
                 y + content_height + PADDING_TOP)
            ]
            self.__draw.rectangle(rect_shape, fill='#868686')
            y += PADDING_TOP
            x += PADDING_LEFT + BORDER_WIDTH
            content_height += PADDING_TOP * 2

        if update_used_space:
            self.used_space += content_height + 30
        self.__draw.multiline_text(
            (x, y),
            text,
            spacing=spacing,
            fill=fg,
            font=font
        )

    @staticmethod
    def __get_template_name(title: str, summary: str, date: str, lang: str) -> str:
        title_font = DefaultStyles().style['title'][lang]['font']
        title_width = DefaultStyles().style['title'][lang]['width']
        title_spacing = DefaultStyles().style['title'][lang]['spacing']
        summary_font = DefaultStyles().style['summary'][lang]['font']
        summary_width = DefaultStyles().style['summary'][lang]['width']
        summary_spacing = DefaultStyles().style['summary'][lang]['spacing']
        date_font = DefaultStyles().style['date'][lang]['font']
        date_spacing = DefaultStyles().style['date'][lang]['spacing']
        new_title = wrap_text(title, title_font, title_width)
        new_summary = wrap_text(summary, summary_font, summary_width)
        content_height = 0
        content_height += title_font.getsize_multiline(
            new_title, spacing=title_spacing)[1] + title_spacing
        content_height += 30
        content_height += date_font.getsize_multiline(
            date, spacing=date_spacing)[1] + date_spacing
        content_height += 30
        content_height += summary_font.getsize_multiline(
            new_summary, spacing=summary_spacing)[1] + summary_spacing
        content_height += 40
        if content_height <= ShortContentStyles().writeable_height:
            return 'short_content', summary
        elif content_height <= RegularStyles().writeable_height:
            return 'regular', summary
        else:
            split_char = '.' if lang == 'en' else to_bijoy('।')
            if summary.endswith(split_char):
                summary = summary[:-1]
            summary = split_char.join(
                summary.split(split_char)[:-1]) + split_char
            return ImageCreator.__get_template_name(title, summary, date, lang)

    def get_image(self):
        return self.__template
