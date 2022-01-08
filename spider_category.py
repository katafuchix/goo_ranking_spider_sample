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
from goo_models import Category


url = 'https://ranking.goo.ne.jp/category/'
response = request.urlopen(url)
soup = BeautifulSoup(response)
response.close()

categories = soup.find('ul', class_='grid-items index-category')
#print(categories)
for li in categories.find_all('li'):
  print(li)
  a = li.find('a')
  print(a.attrs['href'])
  print(a.text)
  print("---------------")
  url = a.attrs['href']
  name = a.text

  r = Category.query.filter(Category.url.contains(url)).all()
  if len(r)>0:
     continue
  
  item = Category(
    name        =  name,
    url         =  url
  )
  db_session.add(item)
  try:
    db_session.flush()
    db_session.commit()
  except:
    db_session.rollback()
    traceback.print_exc()
