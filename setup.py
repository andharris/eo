#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='eo',
    version='0.1.1',
    description='Machine Readable Corpus of US Executive Orders',
    url='https://github.com/andharris/eo',
    author='Andrew Harris',
    license='MIT',
    package_data={
        'eo': ['data/corpus.json']
    },
    install_requires=[
        'bs4',
        'dask',
        'requests',
        'textract'
    ]
)
