import logging

logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)


def log_error(title, message=""):
    logging.error(f"{title.upper()}: {message}")


def log_info(title, message=""):
    logging.info(f"{title.upper()}: {message}")


def log_warning(title, message=""):
    logging.warning(f"{title.upper()}: {message}")
