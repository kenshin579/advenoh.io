#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os
import re
import shutil
import sys
from datetime import datetime
from itertools import islice
from bs4 import BeautifulSoup
import requests

################################################################################################
# todo :
# 1. master 브랜치에 cherry pick을 해야 함 - 자동으로 할 수 없는 방법은 없나?
# - circleci로 가능한지 확인해보기

################################################################################################


################################################################################################
# Constants
#
################################################################################################
BLOG_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
BLOG_CONTENT_DIR = '/'.join([BLOG_DIR, 'content', 'posts'])
README_FILE = os.path.join(BLOG_DIR, 'README.md')
README_HEADER_FILE = '/'.join([BLOG_DIR, 'scripts', 'data', 'HEADER.md'])
BLOG_HOME_URL = 'https://blog.advenoh.pe.kr'

REGEX_SUB_PATTERN = '.*\/blog.advenoh.pe.kr\/content\/posts'
################################################################################################
# Functions
#
################################################################################################

def generate_blog_list():
    result = {}
    for file in get_all_files_with_extension(BLOG_CONTENT_DIR, ['md']):
        category = os.path.basename(os.path.dirname(file)).capitalize()
        if result.get(category):
            result[category].append({'title': get_blog_title(file), 'filename': file})
        else:
            result[category] = [{'title': get_blog_title(file), 'filename': file}]

    write_blog_list_to_file(result, README_FILE)


def get_blog_title(filename):
    with open(filename, 'r') as f:
        for line in islice(f, 1, 2):
            print('line', line)
            return re.findall('title:\\s*\'(.*)\'', line)[0]


def write_blog_list_to_file(result, filename):
    shutil.copyfile(README_HEADER_FILE, README_FILE)

    # write header to the file
    with open(filename, 'a') as out_file:
        out_file.write('\nUpdated ' + datetime.now().strftime('%Y-%m-%d') + '\n\n')
        out_file.write('현재 [블로그](https://blog.advenoh.pe.kr)에 작성된 내용입니다.\n\n')
        for category in sorted(result):
            print('category', category)
            # print('data', result[category])
            out_file.write('## {}\n'.format(category))
            for title_file in sorted(result[category], key=lambda k: k['title']):
                print('title_file', title_file)
                filename = title_file.get('filename')
                # print('filename', filename)

                out_file.write('* [{}]({})\n'.format(
                    title_file.get('title'),
                    re.sub(REGEX_SUB_PATTERN, BLOG_HOME_URL, os.path.splitext(title_file.get('filename'))[0])))
            out_file.write('\n')


def get_all_files_with_extension(path, extensions):
    filenames_with_extension = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            ext = os.path.splitext(filename)[-1]
            for extension in extensions:
                if ext == '.' + extension:
                    filenames_with_extension.append(os.path.join(dirpath, filename))
    return filenames_with_extension


################################################################################################
# Main function
#
################################################################################################


def main():
    parser = argparse.ArgumentParser(description="Maintenance script for my blog")

    parser.add_argument("-g", "--generate", action='store_true',
                        help="Generate blog list for my blog in the readme file")

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()

    print('args', args)

    if args.generate:
        generate_blog_list()

if __name__ == "__main__":
    sys.exit(main())
