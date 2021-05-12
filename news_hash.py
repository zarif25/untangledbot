previous_hashes = {
    'bdnews24.com': "bangladesh-logs-1140-new-virus-cases-death-toll-rises-by-40-in-a-day",
    'www.dhakatribune.com': "barca-title-hopes-hanging-by-a-thread-after-levante-draw"
}

def url_to_hash(url):
    return url.split('/')[-1]