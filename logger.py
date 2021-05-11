import logging

logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)


def log_error(title, message="", sep=":"):
    logging.error(f"{title.upper()}{sep} {message}")


def log_info(title, message="", sep=":"):
    logging.info(f"{title.upper()}{sep} {message}")


def log_warning(title, message="", sep=":"):
    logging.warning(f"{title.upper()}{sep} {message}")
