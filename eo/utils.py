import datetime
import json
import os
import logging

import requests
from bs4 import BeautifulSoup


def page_soup(url):
    resp = requests.get(url)
    if resp.ok:
        return BeautifulSoup(resp.text, 'html.parser')
    else:
        logging.error(' Unable to get {}'.format(url))


def download(url, data_dir=None):
    resp = requests.get(url)
    if resp.ok:
        filepath = os.path.join(data_dir, url.split('/')[-1])
        with open(filepath, 'wb') as f:
            f.write(resp.content)
        return filepath
    else:
        logging.error(' Unable to download file from\n {}'.format(url))


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")
