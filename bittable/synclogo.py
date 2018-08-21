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

class SpiderResult(Base):
    __tablename__ = 'coinmarketcap_logos'
    taskid = Column(String, primary_key=True)
    url = Column(String)
    result = Column(String)
    
    

db = Session()
    
results = db.query(SpiderResult).filter_by().all()
db2 = coinmarketcap.Session()

for res in results:
    
    res_json = json.loads(res.result.decode("utf-8"))
    
    name = res_json.get('name')
    if name is None:
        continue
    slug = name.lower().replace(' ', '-').replace('/','')
    img_url = res_json['logo']
    #print(name, slug, img_url)
    slug_name = slug+"-32x32.png"
    img_name = "img/"+slug_name

    #if not os.path.exists(img_name):
    #    urllib.urlretrieve(img_url, img_name)
    coin = db2.query(MarketCoin).filter_by(name=slug).first()
    if coin:
        coin.logo = img_url 
        coin.src = res_json['src']
        coin.website = res_json['website']
        coin.browser1 = res_json['explorer1']
        coin.browser2 = res_json['explorer2']
        coin.browser3 = res_json['explorer3']
        coin.total_supply = res_json['total_supply']
        print(coin.name, coin.src, coin.browser1)
        db2.add(coin)
        db2.commit()


