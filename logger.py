import logging

logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)


def log_error(title, message="", sep=":"):
    logging.error(__log_message(title, message, sep))


def log_info(title, message="", sep=":"):
    logging.info(__log_message(title, message, sep))


def log_warning(title, message="", sep=":"):
    logging.warning(__log_message(title, message, sep))


def __log_message(title, message, sep):
    if not message:
        sep = ""
    return f"{title.upper()}{sep} {message}"
