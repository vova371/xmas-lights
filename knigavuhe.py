#!/usr/bin/env python

import os
import re
import sys
import json
from urllib.request import urlopen
from urllib.parse import urlparse

from argparse import ArgumentParser

parser = ArgumentParser(description='knigavuhe')
parser.add_argument('-b', '--book', type=str, help='book url')
parser.add_argument('-p', '--path', type=str, default='.', help='output directory')
group = parser.add_mutually_exclusive_group()
group.add_argument('-v', '--verbose', action='store_true', help='increase output verbosity')
group.add_argument('-q', '--quiet', action='store_true', help='suppress console output')
args = parser.parse_args()

directory = args.path

if not os.path.exists(directory):
    os.makedirs(directory)

with urlopen(args.book) as response:
    page = response.read().decode('utf-8')

match = re.search(r'(BookPlayer)\w*\((.*audio.*)\)\w*;', page)

if not match:
    if not args.quiet:
        print('failed to find book player audio files')
    sys.exit(1)

if args.verbose:
    print('book player args: {}'.format(match.group(2)))

book_player_args = json.loads('[' + match.group(2) + ']')

for chapter in book_player_args[1]:
    url = chapter['url']
    name = os.path.basename(urlparse(url).path)
    path = os.path.join(directory, name)

    if not args.quiet:
        print('{} -> {}'.format(url, path))

    with urlopen(url) as response, open(path, 'wb') as output:
        output.write(response.read())
