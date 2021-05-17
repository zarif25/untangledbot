import requests
from logger import log_error, log_warning, log_info


page_id = 104173088514235
access_token = 'EAA6FiKzFv1MBAEJFttTi5hkBN6TbL3rNx9ATFg7Psh1YOCZA15bELbysfu0WZADA9oZAnLDpblvQZAS6FlZAxRWwY05UldU6knrbdZAE0FD54y1MTAiwwpZBmZBv58WgNIs1MLgXiWUqTzZByMCfIilNXs1SQ4jgSC6lZB7ZBCxxJamxP4W2Lh5oJK1'


def post_to_fb(img_url, description, src_url):
    payload = {
        'message': f"{description}\nRead more: {src_url}",
        'url': img_url,
        'access_token': access_token
    }

    r = requests.post(f'https://graph.facebook.com/{page_id}/photos',
                      data=payload)
    log_info("uploaded", f"to fb | {r.json()}")
