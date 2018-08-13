# -*- coding: utf-8 -*-
import datetime
import coinmarketcap
import logging
from time import mktime
import time

SITE='coinmarketcap'

def mkurl(symbol, start, end):
  url = "https://graphs2.coinmarketcap.com/currencies/"+symbol+"/"+str(start)+"/"+str(end)+"/"
  return url

#coinmarketcap.catch_data('coinmarketcap', 'btcusd', url, '5')

def fetch_5min_data(from_date, coin_name):
    #dbsymbol = coinmarketcap.Symbols[symbol]
    #if dbsymbol is None:
    #    logging.error("can't find error symbol " + symbol)
    #    return

    now = datetime.datetime.now()

    last_time = from_date
    i=0
    while True:
        i=i+1
        print(i)
        if last_time > now:
            return
        start_time = last_time 
        end_time = last_time + datetime.timedelta(days=1)
        start = int(mktime(start_time.timetuple()))*1000
        end = int(mktime(end_time.timetuple()))*1000
        url = mkurl(coin_name, start, end)
        print(url)

        coinmarketcap.catch_data(SITE, coin_name, url, 5)
        last_time = end_time
        time.sleep(0.2)
    # sleep(1)


old_day = datetime.datetime.now() - datetime.timedelta(days=7) #6年前
# from_date = datetime.datetime(2013,5,1,0,0,0)
#fetch_5min_data(old_day, 'bitcoin')
fetch_5min_data(old_day, 'eos')

# fetch_5min_data(from_date, 'ethereum')

