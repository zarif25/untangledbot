from image_manip import create_template
import requests

title = "sssssSssssSssssssSssssSssssssSssssSssssssSssssSsa"
description = "ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. ssss ssss. "

src = "The New York Times"

date = "17 May, 2021"

img = requests.get(
    "https://d30fl32nd2baj9.cloudfront.net/media/2019/03/27/ak-momen-aam-03272019-0008.jpg/ALTERNATES/w640/AK-Momen-aam-03272019-0008.jpg",
    stream=True
).raw

post = create_template(title, description*2, src, date, None, 'dark')
post.save('test.png')