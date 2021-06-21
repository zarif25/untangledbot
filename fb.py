import requests

class FbUploadError(Exception):
    pass

class FacebookApi:
    def __init__(self, PAGE_ID: int, ACCESS_TOKEN: str) -> None:
        self.__ACCESS_TOKEN = ACCESS_TOKEN
        self.__url = f'https://graph.facebook.com/{PAGE_ID}/photos'

    def post_image(self, message: str, img_url: str) -> str:
        '''Post image with a message in Facebook

        Args:
            message: message in the Facebook post
            img_url: image of the Facebook post (jpg/png/others)
        Returns:
            id of the post
        '''
        payload = {
            'message': message,
            'url': img_url,
            'access_token': self.__ACCESS_TOKEN
        }
        res = requests.post(self.__url, data=payload).json()
        try:
            return res['id']
        except Exception as e:
            raise FbUploadError(f"Could not upload to facebook. Here is the response: {res}")
