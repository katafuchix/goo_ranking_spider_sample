# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime

class Category(Base):
    __tablename__ = 'categories'
    id          =  Column(Integer, primary_key=True)
    name        =  Column(String(32))
    url         =  Column(String(32), unique=True)
    created_at  =  Column(DateTime)

    def __init__(self, name=None,url=None):
        self.name           =  name
        self.url            =  url
        self.created_at     =  datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class Ranking(Base):
    __tablename__ = 'rankings'
    id          =  Column(Integer, primary_key=True)
    category_id =  Column(Integer)
    name        =  Column(String(256))
    published   =  Column(String(32))
    url         =  Column(String(128))
    url_more    =  Column(String(128))
    created_at  =  Column(DateTime)

    def __init__(self, category_id=0, name=None,url=None,url_more=None):
        self.category_id    =  category_id
        self.name           =  name
        self.url            =  url
        self.url_more       =  url_more
        self.created_at     =  datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class RankingItem(Base):
    __tablename__ = 'ranking_items'
    id          =  Column(Integer, primary_key=True)
    ranking_id  =  Column(Integer)
    rank_order  =  Column(Integer)
    name        =  Column(String(512))
    summary     =  Column(String(512))
    created_at  =  Column(DateTime)

    def __init__(self, ranking_id=0, rank_order=0, name=None, summary=None):
        self.ranking_id     =  ranking_id
        self.rank_order     =  rank_order
        self.name           =  name
        self.summary        =  summary
        self.created_at     =  datetime.now().strftime('%Y-%m-%d %H:%M:%S')
