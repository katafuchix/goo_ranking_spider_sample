from bs4 import BeautifulSoup
from sqlalchemy.orm import joinedload
from db import db_session, init_db
from datetime import datetime
from urllib import request
import time
import sys
import re
import random
import traceback
from goo_models import Category, Ranking



def get_max_pagey(url):
    response = request.urlopen(url)
    soup = BeautifulSoup(response)
    response.close()

    pager = soup.find('ol', class_='nav-pager')
    pages = []
    for li in pager.find_all('li'):
      #print(li)
      try:
        pages.append(int(li.text))
      except:
        continue

    if len(pages) == 0:
        return 0
    return max(pages)

def get_url_more(url):
    response = request.urlopen(url)
    soup = BeautifulSoup(response)
    response.close()

    try:
        a= soup.find('a', id='column_goranking_pcbtn')
        return a.attrs['href']
    except:
        return ""

def get_links(category_id, url):
    #response = request.urlopen(url)
    #soup = BeautifulSoup(response)
    #response.close()
    print(url)
    req = request.Request(url)
    #リクエストを発行し、HTMLデータを受け取る
    html = request.urlopen(req)
    #HTMLデータをBeautifulSoupに解釈される
    soup = BeautifulSoup(html, "html.parser")
    h3 = soup.find_all('h3')
    #print(h3)
    for item in h3[::-1]:
        name = item.text
        url  = item.find('a').get('href')
        print(name)
        print(url)
        r = Ranking.query.filter(Ranking.url.contains(url)).all()
        if len(r)>0:
            continue

        url_more = get_url_more('https://ranking.goo.ne.jp{}'.format(url))
        print('https://ranking.goo.ne.jp{}'.format(url))
        print(url_more)

        item = Ranking(
            category_id =  category_id,
            name        =  name,
            url         =  url,
            url_more    = url_more
        )
        db_session.add(item)
        try:
            db_session.flush()
            db_session.commit()
        except:
            db_session.rollback()
            #traceback.print_exc()

categories = db_session.query(Category).all()
for category in categories:
    print(category.name)
    url = 'https://ranking.goo.ne.jp{}'.format(category.url)
    #print( get_max_pagey(url) )

    # 初期の場合
    #max_page = get_max_pagey(url)

    # cron
    max_page = 1
    print(max_page)
    if max_page > 0:
        page_list = list(range(1, max_page+1))
        print(page_list[::-1])
        for i in page_list[::-1]:
            page_url = "{}?page={}".format(url, i)
            get_links(category.id, page_url)
    else:
        get_links(category.id, url)
