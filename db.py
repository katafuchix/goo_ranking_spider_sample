# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class RepresentableBase(object):
    def __repr__(self):
        """Dump all columns and value automagically.

        This code is copied a lot from followings.
        See also:
           - https://gist.github.com/exhuma/5935162#file-representable_base-py
           - http://stackoverflow.com/a/15929677
        """
        #: Columns.
        columns = ', '.join([
            '{0}={1}'.format(k, repr(self.__dict__[k]))
            for k in self.__dict__.keys() if k[0] != '_'
        ])

        return '<{0}({1})>'.format(
            self.__class__.__name__, columns
        )

engine = create_engine('mysql+pymysql://[MYSQL_USER]:[MYSQL_USER_PASSWORD]@[MYSQL_SEARVER]/[MYSQL_DB_NAME]?charset=utf8mb4', convert_unicode=True)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base(cls=RepresentableBase)
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)
