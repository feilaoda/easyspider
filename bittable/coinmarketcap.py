# -*- coding: utf-8 -*-

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
import datetime
import json
from decimal import Decimal


engine = create_engine("mysql+mysqlconnector://root:Sanquan2018!@192.168.0.232/bittable?charset=utf8")
#engine = create_engine("mysql+mysqlconnector://root:admin@localhost/bittable?charset=utf8")

Session = sessionmaker(bind=engine, autoflush=True, autocommit=False)



ScopedSession = scoped_session(sessionmaker(bind=engine, autoflush=True, autocommit=False))
class BaseClass(object):
    query =  ScopedSession.query_property()
    def commit(self):
        db = ScopedSession()
        db.add(self)
        db.commit()        

Base = declarative_base(cls=BaseClass)

class MarketSite(Base):
    __tablename__ = 'market_site'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
Cookies = ''

class MarketSymbol(Base):
    __tablename__ = 'market_symbol'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
   
class MarketCoin(Base):
    __tablename__ = 'market_coin'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    title = Column(String)
    symbol = Column(String)
    #uri = Column(String)
    logo = Column(String)
    rank = Column(String)
    market_cap = Column(BigInteger)
    price = Column(DECIMAL(precision=18,scale=8))
    volume = Column(BigInteger)
    supply = Column(BigInteger)
    total_supply = Column(BigInteger)
    change24h = Column(DECIMAL)
    change12h = Column(DECIMAL)
    change6h = Column(DECIMAL)
    change4h = Column(DECIMAL)
    change2h = Column(DECIMAL)
    change1h = Column(DECIMAL)
    src = Column(String)
    website = Column(String)
    browser1 = Column(String)
    browser2 = Column(String)
    browser3 = Column(String)
    #change7d = Column(DECIMAL)
    updated_at = Column(DateTime, default=datetime.datetime.now())
     

class MarketTradeMin(Base):
    __tablename__ = 'market_trade_min'
    id = Column(BigInteger, primary_key=True)
    symbol_id = Column(Integer)
    site_id = Column(Integer)
    coin_id = Column(Integer)
    tid = Column(BigInteger)
    data_type = Column(Integer)
    market_cap = Column(BigInteger)
    price = Column(DECIMAL(precision=18,scale=8))
    price_date = Column(BigInteger)
    price_btc = Column(DECIMAL(precision=18,scale=8))
    price_usd = Column(DECIMAL(precision=18,scale=8))
    price_open = Column(DECIMAL(precision=18,scale=8))
    price_close = Column(DECIMAL(precision=18,scale=8))
    price_high = Column(DECIMAL(precision=18,scale=8))
    price_low = Column(DECIMAL(precision=18,scale=8))
    volume = Column(BigInteger)
    created_at = Column(DateTime, default=datetime.datetime.now())



def http_fetch(url, headers={}, timeout=20, proxies=None):
    logging.debug("Download start ======== %s, %s" % (url,type(url)))

    try:
        result = dict()
        response = requests.get(url, headers=headers, timeout=timeout, proxies=proxies)
        # logging.debug("requests response encoding =============== ************* %s" % response.encoding)
        if response.status_code != requests.codes.ok:
            return dict(code=response.status_code)

        html = response.content

        if 'Set-Cookie' in response.headers:
            cookies = response.headers['Set-Cookie']
            result['set-cookie'] = cookies
        content_type = response.headers.get('content-type')
        result['content-type'] = content_type
        result['code'] = response.status_code
        result['content'] = html
        result['url'] = response.url
        result['old_url'] = url
        if content_type == '':
            result['doc'] = PyQuery(html)
        # logging.debug("Download end ======== [%s] %d" % (url, response.status_code))
        return result

    except Exception as e:
        logging.error("fetch url:%s get error \n%s" % (url,traceback.format_exc()))
        return dict(code=-1)

    return dict(code=-1)


Headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

def catch_data(site_name, coin_name, url, data_type):
    db = Session()
    site = db.query(MarketSite).filter_by(name=site_name).first()
    coin = db.query(MarketCoin).filter_by(name=coin_name).first()
    if site is None or coin is None:
        logging.error("error site or coin %s %s", site_name, coin_name)
        return
    res = http_fetch(url,headers=Headers)
    if res['code'] != 200:
        logging.error("url return " + str(res['code']))
        return

    print("coin:", coin.id, site.id)
    content = res['content']

    prices = []
    if content is not None:
        content_json = json.loads(content)
        #print(content_json)
        market_cap = content_json['market_cap_by_available_supply']
        price_btc = content_json['price_btc']
        price_usd = content_json['price_usd']
        volume = content_json['volume_usd']
        market_cap_dict = {}
        for cap in market_cap:
            market_cap_dict[cap[0]] = cap[1]
        usd_dict = {}
        for usd in price_usd:
            usd_dict[usd[0]] = usd[1]
        volume_dict = {}
        for v in volume:
            volume_dict[v[0]] = v[1]
        #print(usd_dict)
        #print(volume_dict)

        for btc in price_btc:
            price = []
            key = btc[0]
            price.append(btc[0])
            price.append(btc[1])
            price.append(usd_dict[key])
            price.append(volume_dict[key])
            price.append(market_cap_dict[key])
            prices.append(price)


    print("len prices:", len(prices))
    for price in prices:
        t = price[0]
        format_time = int(t/(300*1000))*1000*300 + 299*1000
        btc_price = price[1]
        usd_price = price[2]
        volume = price[3]
        cap = price[4]
        data = db.query(MarketTradeMin).filter_by(coin_id=coin.id, site_id=site.id, tid=format_time, data_type=data_type).first()
        if data is None:
            trade = MarketTradeMin()
            trade.coin_id = coin.id
            trade.site_id = site.id
            trade.tid = format_time
            trade.market_cap = cap
            trade.data_type = data_type
            trade.price_date = datetime.datetime.fromtimestamp(int(format_time/1000))
            trade.price_btc = '{0:.8f}'.format(Decimal(btc_price))
            trade.price_usd = usd_price
            trade.price_open = usd_price
            trade.price_close = usd_price
            trade.price_high = usd_price
            trade.price_low = usd_price
            trade.volume = volume
            trade.created_at = datetime.datetime.fromtimestamp(int(t/1000))
            db.add(trade)
        else:
            # print(type(data.price_usd), type(usd_price))
            db_price = '{0:.2f}'.format(data.price_usd)
            new_price = '{0:.2f}'.format(usd_price)
            if db_price != new_price:
                data.price_usd = usd_price
                data.price_open = usd_price
                data.price_close = usd_price
                data.price_high = usd_price
                data.price_low = usd_price
                data.created_at = datetime.datetime.fromtimestamp(int(t/1000))
                db.add(data)
                print("data is not none, update it.",data.price_usd, usd_price,db_price,new_price, format_time, data_type, datetime.datetime.fromtimestamp(int(t/1000)), datetime.datetime.fromtimestamp(int(format_time/1000)))
            else:
                print("data is not none", format_time, data_type, datetime.datetime.fromtimestamp(int(format_time/1000)))
    db.commit()
    db.close()
    # print(prices)
    


Symbols={
    "bitcoin":"btcusd",
    "ethereum":"ethusd",
    "eos":"eosusd",
}
