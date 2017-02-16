import json
import os
import pkg_resources

from eo import archives
from eo import whitehouse
from eo import utils


CORPUS = pkg_resources.resource_filename('eo', 'data/corpus.json')


def create():
    wh = whitehouse.corpus()
    ar = archives.corpus()
    return wh + ar


def save(corpus, output_dir='data'):
    with open(os.path.join(output_dir, 'corpus.json'), 'w') as output:
        json.dump(corpus, output, indent=4, default=utils.datetime_handler)


def load():
    with open(CORPUS) as data_file:
        return json.load(data_file)


def update():
    ar = [eo for eo in load()
          if eo.get('president') != 'Donald J. Trump']
    wh = whitehouse.corpus()
    return ar + wh
