from datetime import datetime

import dask.bag as db

from eo.utils import page_soup


WHITEHOUSE = 'https://www.whitehouse.gov'


def pages(page='/briefing-room/presidential-actions/executive-orders'):
    soup = page_soup(WHITEHOUSE + page)
    eos = [eo.a.get('href') for eo in soup.find_all('h3', {'class': 'field-content'})]
    n_pages = soup.find('li', {'class': 'pager-current'}).text.split(' ')[-1]
    for page_num in range(1, int(n_pages)):
        soup = page_soup(WHITEHOUSE + page + '?page={}'.format(page_num))
        eos += [eo.a.get('href') for eo in soup.find_all('h3', {'class': 'field-content'})]
    return eos


def text(soup):
    eo = soup.find('div', {'class': 'field-items'})
    return ' '.join(eo.stripped_strings)


def format_date(soup):
    date = soup.find('div', {'class': 'press-article-date'}).text
    return datetime.strptime(date, '%B %d, %Y')


def corpus():
    soups = db.from_sequence([(WHITEHOUSE + eo, page_soup(WHITEHOUSE + eo))
                              for eo in pages()])
    return [{'president': 'Donald J. Trump',
             'eo': None,
             'date': format_date(soup),
             'url': url,
             'text': text(soup)}
            for url, soup in soups]
