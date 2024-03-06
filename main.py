import random

import requests as r
from requests import HTTPError
from bs4 import BeautifulSoup

DATA_SOURCE = 'https://mimuw.fandom.com/pl/wiki/Specjalna:Wszystkie_strony'
LIMIT = 6

if __name__ == '__main__':
    rq = r.get(DATA_SOURCE)
    if rq.ok:
        # print(rq.text)
        soup = BeautifulSoup(rq.text, 'html.parser')
        posts_gen = soup.find(id='mw-content-text').find(class_='mw-allpages-chunk').descendants
        posts = []
        for p in posts_gen:
            if p.name == 'a':
                posts.append(p)

        print('[*] Found {} elements'.format(len(posts)))

        ch = random.choices(posts, k=LIMIT)
        for c in ch:
            print(c)

    else:
        raise HTTPError('Request failed' + rq.status_code)
