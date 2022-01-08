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

r = Ranking.query.filter(Ranking.published == (None)).all()
for item in r:
    print(item)

    url = 'https://ranking.goo.ne.jp{}'.format(item.url_more)
    response = request.urlopen(url)
    soup = BeautifulSoup(response)
    response.close()

    try:
        post_date = soup.find('p', class_='post-date')
        print(post_date.text.strip().split("\n"))
        published = post_date.text.strip().split("\n")[0]
        print(published)
        item.published = published
        print(published)

        db_session.add(item)
        try:
            db_session.flush()
            db_session.commit()
        except:
            db_session.rollback()

    except:
        continue
