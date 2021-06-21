import base64

import requests


class ImgbbUploadError(Exception):
    pass


class ImgbbApi():
    def __init__(self, KEY: int) -> None:
        self.__KEY = KEY

    def upload_image(self, img_path):
        '''
        Uploads story image to imgbb

        Args:
            img_path: path of image to upload

        Returns:
            url of the uploaded image
        '''
        with open(img_path, "rb") as img_file:
            image = base64.b64encode(img_file.read())
        payload = {
            "key": self.__KEY,
            "image": image,
            "expiration": 600
        }
        url = "https://api.imgbb.com/1/upload"
        try:
            res = requests.post(url, payload)
            uploaded_url = res.json()['data']['url']
            return uploaded_url
        except Exception as e:
            raise ImgbbUploadError(f"Could not upload to imgbb because: {e}")
