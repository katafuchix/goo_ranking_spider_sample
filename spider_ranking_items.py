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
from goo_models import Category, Ranking, RankingItem

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

def get_items(ranking_id, url):
    print(url)
    req = request.Request(url)
    #リクエストを発行し、HTMLデータを受け取る
    html = request.urlopen(req)
    #HTMLデータをBeautifulSoupに解釈される
    soup = BeautifulSoup(html, "html.parser")
    dl = soup.find('dl', class_='main-ranking')
    uls = dl.find_all('li')

    for ul in uls:
      ranking_number = ul.find('div', class_='ranking-number')
      if ranking_number == None:
        continue
      rank_order = ranking_number.text.strip().replace('位', '')
      print(rank_order)

      content = ranking_number = ul.find('div', class_="ranking-content")
      name = content.find('h2').text.strip()
      summary = content.find('p', class_="summary").text.strip()
      print(name)
      print(summary)
      print("=======")
      item = RankingItem(
        ranking_id  =  ranking_id,
        rank_order  =  rank_order,
        name        =  name,
        summary     =  summary
      )
      db_session.add(item)
      try:
        db_session.flush()
        db_session.commit()
      except:
        db_session.rollback()


rankings = db_session.query(Ranking).order_by(Ranking.id.desc()).all()
for ranking in rankings:
    print(ranking.name)
    if ranking.url_more == '' or ranking.published == '':
        continue

    url = 'https://ranking.goo.ne.jp{}'.format(ranking.url_more)
    #print( get_max_pagey(url) )

    r = RankingItem.query.filter(RankingItem.ranking_id.contains(ranking.id)).all()
    print(len(r))
    if len(r)>10:
        continue

    max_page = get_max_pagey(url)
    print(max_page)
    if max_page > 0:
        page_list = list(range(1, max_page+1))
        print(page_list)
        for i in page_list:
            page_url = "{}?page={}".format(url, i)
            print(page_url)
            get_items(ranking.id, page_url)
    else:
        print(0)
        get_items(ranking.id, url)
