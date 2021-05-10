def update_hash(latest_hash):
    with open('previous_hash.txt', 'w') as rw:
        rw.truncate(0)
        rw.write(latest_hash)


def get_prev_hash():
    with open('previous_hash.txt', 'r') as rf:
        return rf.read()


def url_to_hash(url):
    return url.split('/')[-1]