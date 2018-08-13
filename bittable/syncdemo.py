import os
import json
import datetime
from decimal import Decimal
import urllib
from sqlalchemy import create_engine
import logging
import requests
import traceback
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy import Column, DateTime, String, Integer,  ForeignKey, func
from sqlalchemy.types import BigInteger, DECIMAL,Numeric
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.dialects.mysql import MEDIUMBLOG

import coinmarketcap
from coinmarketcap import MarketCoin

engine = create_engine("mysql+mysqlconnector://root:admin@localhost/bittable_resultdb?charset=utf8")

Session = sessionmaker(bind=engine, autoflush=True, autocommit=False)

ScopedSession = scoped_session(sessionmaker(bind=engine, autoflush=True, autocommit=False))
class BaseClass(object):
    query =  ScopedSession.query_property()
    def commit(self):
        db = ScopedSession()
        db.add(self)
        db.commit()        

Base = declarative_base(cls=BaseClass)

class AbsShardingClass(Base):
   __abstract__ = True
  

def get_result_class(table_name):
    DynamicBase = declarative_base(class_registry=dict())
    class SpiderResult(DynamicBase):
        __tablename__ = table_name
        taskid = Column(String, primary_key=True)
        url = Column(String)
        result = Column(String)
    return SpiderResult

def get_class_name_and_table_name(hashid):
    return SpiderResult, hashid # 'ShardingClass%s' % hashid, 'sharding_class_%s' % hashid

ENTITY_CLASS_DICT = {}

def get_sharding_entity_class(hashid):
    """
    @param hashid: hashid
    @type hashid: int
    @rtype AbsClientUserAuth
    """

    if hashid not in ENTITY_CLASS_DICT:
        class_name, table_name = get_class_name_and_table_name(hashid)
        cls = type(class_name, (SpiderResult,),
                   {'__tablename__': table_name})
        ENTITY_CLASS_DICT[hashid] = cls

    return ENTITY_CLASS_DICT[hashid]
    

db = Session()
    
clz1 = get_result_class('coinmarketcap_logos')
results = db.query(clz1).filter_by().first()
print(results.url)

clz2 = get_result_class('coinmarketcap_allcoins')
results = db.query(clz2).filter_by().first()
print(results.url)

# cls = get_sharding_entity_class("coinmarketcap_logos")
# print db.query(cls).get(1)

