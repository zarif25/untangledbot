previous_hashes = {
    'bdnews24.com': "vegas-style-weddings-land-in-brooklyn",
    'www.dhakatribune.com': "eid-holiday-rush-leads-to-12km-tailback-on-dhaka-aricha-highway"
}

def url_to_hash(url):
    return url.split('/')[-1]