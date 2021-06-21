from datetime import datetime
BN_DIGITS = "০১২৩৪৫৬৭৮৯"


def to_en_digit(digit: str):
    return BN_DIGITS.find(digit)


def to_en_num(num: str):
    return int(''.join(str(to_en_digit(digit)) for digit in num))


def to_en_month(month: str):
    return {
        "জানুয়ারি": 1,
        "ফেব্রুয়ারী": 2,
        "মার্চ": 3,
        "এপ্রিল": 4,
        "মে": 5,
        "জুন": 6,
        "জুলাই": 7,
        "আগষ্ট": 8,
        "সেপ্টেম্বর": 9,
        "অক্টোবর": 10,
        "নভেম্বর": 11,
        "ডিসেম্বর": 12,
    }[month]


def to_en_datetime(dtime: str, format="dd mmmm, yyyy") -> datetime:
    if format == "dd mmmm, yyyy":
        day_month, year = dtime.split(',')
        year = to_en_num(year.strip())
        month = to_en_month(day_month[3:])
        day = to_en_num(day_month[:2])
        return datetime(year, month, day)
