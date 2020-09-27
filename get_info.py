# -*- coding: utf-8 -*-
import json
import os
import time

import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

with open('slug.txt', 'a') as f:
    for i in range(1, 378):
        r = requests.get(
            f'https://www.epub.vn/categories?page={i}',
            headers={
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
                'referer': 'https://www.epub.vn/',
                'accept-language': 'en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7',
            })
        soup = BeautifulSoup(r.content.decode('utf-8'), 'html.parser')

        for cover_div in soup.find_all("div", class_="cover"):
            f.write(f"{cover_div.find('a').get('href')}\n")
            f.flush()

f.close()

# export PYTHONIOENCODING=utf-8
