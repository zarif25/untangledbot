import requests
import base64
from logger import log_info


def upload_to_imgbb(path):
    with open(path, "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": "13f9115b9e666db5b88b10eb11c74e9f",
            "image": base64.b64encode(file.read()),
            "expiration": 600
        }
        res = requests.post(url, payload)
        uploaded_url = res.json()['data']['url']
        log_info("uploaded", f"to imgbb | {uploaded_url}")
        return uploaded_url
