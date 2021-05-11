from time import localtime

def get_theme():
    t_hour = (localtime().tm_hour + 6) % 24
    return 'light' if 3 <= t_hour <= 18 else 'dark'