from logger import log_info
from fb_graph_api import GraphAPI
from os import getenv

page_id = 104173088514235
access_token = getenv("FBTOKEN")

# page_id = 103167858653625
# access_token = "EAANOwCCZAVKsBAPkEzgNS4KIvxhi98tFiUIhdkwBDoBZBrvI5tZBhlvOycptWGQTY6WZAuu7PsjfKIOFnQYIxlXSHol1exraINVFCAudfkV1HZBTKa0bDZBR32XlWEfQVdI8GtmkZB3XAQCyuJ0jqCzt5RmP8ZB8ZAkO8TwFVT4mVvAhkpOrGVQGkLP5MwtpGvasO8iASyjFy298MDBo8p24T"

fb_api = GraphAPI(page_id, access_token)

def post_to_fb(img_url, title, description, src_url):
    message = f"{title}\n\n{description}\n\nRead more: {src_url}"
    res = fb_api.post_img(message, img_url)
    log_info("uploaded", f"to fb | {res}")
