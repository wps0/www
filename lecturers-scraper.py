import os.path
import random
import re

import requests as r
from requests import HTTPError
from bs4 import BeautifulSoup
from jinja2 import Environment, PackageLoader, select_autoescape
from urllib.parse import urljoin
from duckduckgo_search import DDGS

BASE_URL = 'https://mimuw.fandom.com'
DATA_SOURCE = urljoin(BASE_URL, '/pl/wiki/Specjalna:Wszystkie_strony')
LIMIT = 2
PUBLIC_DIR = 'public/'


class Entity:
    name: str
    img: str
    img_title: str
    more_url: str
    desc: str
    exported_url: str

    def __init__(self, name: str, img: str, img_title: str, desc: str):
        self.name = name
        self.img = img
        self.img_title = img_title
        self.desc = desc
        self.more_url = None

    def as_markdown(self, template):
        print(self.__dict__)
        return template.render(self.__dict__)

    def __repr__(self):
        return f'{self.name} ({self.img}: {self.img_title}) - {self.desc}'


def log(*args):
    print('[*]', *args)


def log_progress(*args):
    print('[~]', *args)


def get_more_details(url):
    log_progress('Getting more details for', url)
    soup = BeautifulSoup(r.get(url).text, 'html.parser')
    details = (soup.find(id='mw-content-text')
               .find(class_='mw-parser-output'))

    for link in soup.select('a'):
        link.extract()

    print(details)
    log('OK')
    return details


if __name__ == '__main__':
    rq = r.get(DATA_SOURCE)
    if rq.ok:
        soup = BeautifulSoup(rq.text, 'html.parser')
        posts_gen = soup.find(id='mw-content-text').find(class_='mw-allpages-chunk').descendants
        posts = []
        for p in posts_gen:
            if p.name == 'a':
                posts.append(p)

        log('Found {} elements'.format(len(posts)))

        rng_lecturers = random.choices(posts, k=LIMIT)
        lecturers = []
        for l in rng_lecturers:
            lecturers.append(Entity(
                l.string,
                None,
                None,
                get_more_details(urljoin(BASE_URL, l['href']))
            ))

        log_progress('Getting images & additional info...')
        for l in lecturers:
            q = l.name + ' MIMUW'
            log_progress('Querying', q)

            res = DDGS().text(q, region='pl-pl', max_results=1)[0]
            # print(res)
            l.more_url = res['href']

            res = DDGS().images(q, region='pl-pl', max_results=1)[0]
            # print(res)
            l.img = res['image']
            l.img_title = res['title']
            log('OK')

        log_progress('Exporting the templates')
        env = Environment(
            loader=PackageLoader(
                package_name='lecturers-scraper',
                package_path='templates'),
            autoescape=select_autoescape())
        entity_tmpl = env.get_template('entity_page.md')
        index_tmpl = env.get_template('index.md')

        for l in lecturers:
            filename = re.sub(r'[^\d.a-zA-Z]', '_', l.name)
            l.exported_url = filename + '.html'
            filename += '.md'

            with open(os.path.join(PUBLIC_DIR, filename), 'w') as f:
                f.write(l.as_markdown(entity_tmpl))

        with open(os.path.join(PUBLIC_DIR, 'index.md'), 'w') as f:
            f.write(index_tmpl.render(entities=lecturers))

        log('OK')
    else:
        raise HTTPError('Request failed' + rq.status_code)
