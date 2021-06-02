import requests

class GraphAPI:
    def __init__(self, page_id: int, access_token: str) -> None:
        self.__access_token = access_token
        self.__url = f'https://graph.facebook.com/{page_id}/photos'
    
    def post_img(self, message: str, img_url: str) -> str:
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
            'access_token': self.__access_token
        }
        return requests.post(self.__url, data=payload).json()['id']