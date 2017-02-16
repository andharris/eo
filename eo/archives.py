import logging
import os
import shutil
from datetime import datetime

import textract
import dask.bag as db

from eo import utils


ARCHIVES = 'https://www.archives.gov'
DATA_DIR = '.EO_PDFs'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


def presidents(pagepath='/federal-register/executive-orders/disposition.html'):
    soup = utils.page_soup(ARCHIVES + pagepath)
    return db.from_sequence(
        [(p.text.replace('\xa0', ' ').replace('\n', ''), p.a.get('href'))
        for p in soup.find_all('strong')
        if p.a]
    )


def years(president, pagepath):
    soup = utils.page_soup(ARCHIVES + pagepath)
    return (president, db.from_sequence([a.get('href')
                                         for a in soup.find_all('a')
                                         if a.text.isdigit()]))


def eos(president, years):
    def year_eos(year, president=None):
        soup = utils.page_soup(ARCHIVES + year)
        eos = (soup.find('section', {'class': 'block block-system clearfix'})
                   .find_all('hr'))
        return db.from_sequence([process(president, eo)
                                 for eo in eos
                                 if eo.find('a')])

    return years.map(year_eos, president=president)


def process(president, eo):
    date = format_date(eo)
    num = (eo.find('a').attrs.get('name')
           if eo.find('a') else None)
    if eo.find('a', {'class': 'pdfImage'}):
        pdf = eo.find('a', {'class': 'pdfImage'}).get('href')
        if pdf.startswith('/'):
            url = ARCHIVES + pdf
        else:
            url = pdf
        text = extract_text(utils.download(url, DATA_DIR))
    else:
        logging.info(' No PDF for EO: {}'.format(num))
        url = None
        text = None

    return {
        'president': president,
        'eo': num,
        'date': date,
        'url': url,
        'text': text
    }


def format_date(eo):
    signed = [li.text.replace('Signed:', '').strip()
              for li in eo.find_all('li')
              if li.text.startswith('Signed:')]
    if signed:
        try:
            return datetime.strptime(signed[0], '%B %d, %Y')
        except ValueError:
            logging.warn((' Unable to parse date signed ({}) for EO: {}'
                           .format(signed[0], eo.find('a').attrs.get('name'))))
    else:
        logging.info(' Unable to determine signed date')


def extract_text(filepath):
    if filepath:
        return str(textract.process(filepath))


def corpus():
    tasks =  presidents().map(years).map(eos)
    data = [eos
            for presidents in tasks
            for years in presidents
            for eos in years]
    shutil.rmtree(DATA_DIR)
    return data
