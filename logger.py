import logging

logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)
logs = {
    'E': [],
    'I': [],
    'W': []
}

def log_error(title, message=""):
    log_str = f"{title.upper()}: {message}"
    logs['E'].append(log_str)
    logging.error(log_str)


def log_info(title, message=""):
    log_str = f"{title.upper()}: {message}"
    logs['I'].append(log_str)
    logging.info(log_str)


def log_warning(title, message=""):
    log_str = f"{title.upper()}: {message}"
    logs['W'].append(log_str)
    logging.warning(log_str)
