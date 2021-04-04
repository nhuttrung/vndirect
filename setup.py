#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# VNDirect market data downloader
# https://github.com/nhuttrung/vndirect

from setuptools import setup, find_packages
import io
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with io.open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='vndirect',
    version="0.5.0",
    description='VNDirect market data downloader',
    long_description=long_description,
    url='https://github.com/nhuttrung/vndirect',
    author='Trung N. Tran',
    author_email='trannhuttrung@gmail.com',
    license='Apache',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 5 - Production/Stable',


        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Office/Business :: Financial',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    platforms=['any'],
    keywords='pandas, pandas datareader, vn30',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'examples']),
    install_requires=['pandas>=0.24', 'numpy>=1.15', 'requests>=2.20'],
    entry_points={
        'console_scripts': [
            'sample=sample:main',
        ],
    },
)
