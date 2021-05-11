import requests
import logging

logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)

page_id = 104173088514235
access_token = 'EAA6FiKzFv1MBAEJFttTi5hkBN6TbL3rNx9ATFg7Psh1YOCZA15bELbysfu0WZADA9oZAnLDpblvQZAS6FlZAxRWwY05UldU6knrbdZAE0FD54y1MTAiwwpZBmZBv58WgNIs1MLgXiWUqTzZByMCfIilNXs1SQ4jgSC6lZB7ZBCxxJamxP4W2Lh5oJK1'


def post_to_fb(img_url, description):
    img_payload = {
        'message': description,
        'url': img_url,
        'access_token': access_token
    }

    r = requests.post(
        f'https://graph.facebook.com/{page_id}/photos', data=img_payload)
    logging.info(f"uploaded to fb | {r.text}")
