#!/usr/bin/env python

import os
import re
import sys
import json
from urllib.request import urlopen
from urllib.parse import urlparse

from argparse import ArgumentParser

parser = ArgumentParser(description='knigavuhe')
parser.add_argument("--book", type=str, help='book url')
parser.add_argument("--path", type=str, default='.', help='output directory')
args = parser.parse_args()

directory = args.path

if not os.path.exists(directory):
    os.makedirs(directory)

with urlopen(args.book) as response:
    page = response.read().decode('utf-8')

match = re.search(r"(BookPlayer)[^;]*(\[.*audio[^\]]*\])", page)

if not match:
    print('failed to find book chapters')

chapters = json.loads(match.group(2))

for chapter in chapters:
    url = chapter['url']
    name = os.path.basename(urlparse(url).path)
    path = os.path.join(directory, name)
    print('{} -> {}'.format(url, path))
    with urlopen(url) as response, open(path, 'wb') as output:
        output.write(response.read())
