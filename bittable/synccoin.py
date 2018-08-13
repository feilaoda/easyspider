from decimal import Decimal

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
    __tablename__ = 'coinmarketcap_allcoins'
    taskid = Column(String, primary_key=True)
    url = Column(String)
    result = Column(String)
    

db = Session()
db2 = coinmarketcap.Session()

result = db.query(SpiderResult).filter_by().first()


data_json = json.loads(result.result.decode("utf-8"))
rank = 1
for coin in data_json['data']:
    name = coin['name']
    name = name.lower().replace(' ', '-').replace('/','')
    mc = MarketCoin()
    newmc = db2.query(MarketCoin).filter_by(name=name).first()
    if newmc is None:
        mc.name = name
    else:
        mc = newmc
    mc.title = coin['name']
    mc.symbol = coin['symbol']
    price = Decimal(coin['price'])
    mc.price = '{0:.8f}'.format(price)
    mc.market_cap = coin['market_cap']
    mc.volume = coin['volume']
    mc.supply = coin['supply']
    #mc.uri = "/market/currency/"+mc.name
    mc.rank = rank
    rank = rank + 1
    mc.change1h = '{0:.4f}'.format(Decimal(coin['change1h']))
    mc.change24h = '{0:.4f}'.format(Decimal(coin['change24h']))
    mc.change7d = '{0:.4f}'.format(Decimal(coin['change7d']))
    mc.updated_at = datetime.datetime.now()
    print(coin)
    db2.add(mc)

db2.commit()
db2.close()
