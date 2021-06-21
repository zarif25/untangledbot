from datetime import datetime
BN_DIGITS = "০১২৩৪৫৬৭৮৯"


def to_bn_digit(digit: int):
    return BN_DIGITS[digit]


def to_bn_num(num: int):
    str_num = str(num)
    return ''.join(to_bn_digit(int(digit)) for digit in str_num)


def to_bn_month(month: int):
    return {
        1: "জানুয়ারি",
        2: "ফেব্রুয়ারী",
        3: "মার্চ",
        4: "এপ্রিল",
        5: "মে",
        6: "জুন",
        7: "জুলাই",
        8: "আগষ্ট",
        9: "সেপ্টেম্বর",
        10: "অক্টোবর",
        11: "নভেম্বর",
        12: "ডিসেম্বর"
    }[month]


def to_bn_week(weekday: int):
    return {
        0: "সোমবার",
        1: "মঙ্গলবার",
        2: "বুধবার",
        3: "বৃহস্পতিবার",
        4: "শুক্রবার",
        5: "শনিবার",
        6: "রবিবার"
    }[weekday]


def to_bn_datetime(datetime: datetime):
    week = to_bn_week(datetime.weekday())
    month = to_bn_month(datetime.month)
    day = to_bn_num(datetime.day)
    year = to_bn_num(datetime.year)
    return f"{week}, {month} {day}, {year}"
