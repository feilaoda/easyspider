# -*- coding: utf-8 -*-
import datetime
import coinmarketcap
import logging
from time import mktime
import time
import os
from mq import build_queue

from apscheduler.schedulers.blocking import BlockingScheduler


data_queue = build_queue(qname="q_coinmarketcap_5min", host='192.168.0.241', port=6379)



SITE='coinmarketcap'

def mkurl(symbol, start, end):
  url = "https://graphs2.coinmarketcap.com/currencies/"+symbol+"/"+str(start)+"/"+str(end)+"/"
  return url

#coinmarketcap.catch_data('coinmarketcap', 'btcusd', url, '5')

def make_date(from_date, delta_days, coin_name):
    start_time = from_date
    end_time = start_time + datetime.timedelta(days=delta_days)
    start = int(mktime(start_time.timetuple()))*1000
    end = int(mktime(end_time.timetuple()))*1000
    url = mkurl(coin_name, start, end)

    return (end_time, url)

def fetch_5min_data(from_date, coin_name):
    now = datetime.datetime.now()
    last_time = from_date
    i=0
    while True:
        i=i+1
        print(i)
        if last_time > now:
            return
        start_time = last_time 
        end_time, url = make_date(start_time, 1, coin_name)
        # end_time = last_time + datetime.timedelta(days=1)
        # start = int(mktime(start_time.timetuple()))*1000
        # end = int(mktime(end_time.timetuple()))*1000
        # url = mkurl(coin_name, start, end)
        print(url)

        prices = coinmarketcap.catch_data(SITE, coin_name, url, 5)
        if prices is not None and len(prices) > 0:
            qdata = {'site': "coinmarketcap", 'currency':coin_name, 'prices': prices}
            data_queue.put(qdata)

        last_time = end_time
        time.sleep(0.2)


def fetch_7d_data(from_date, coin_name):
    now = datetime.datetime.now()
    last_time = from_date
    i=0
    while True:
        i=i+1
        print(i)
        if last_time > now:
            return
        start_time = last_time 
        end_time, url = make_date(start_time, 30, coin_name)
        # end_time = last_time + datetime.timedelta(days=1)
        # start = int(mktime(start_time.timetuple()))*1000
        # end = int(mktime(end_time.timetuple()))*1000
        # url = mkurl(coin_name, start, end)
        print(url)

        prices = coinmarketcap.catch_data(SITE, coin_name, url, 60)
        # if len(prices) > 0:
        #     qdata = {'site': "coinmarketcap", 'currency':coin_name, 'prices': prices}
        #     data_queue.put(qdata)

        last_time = end_time
        time.sleep(0.2)

def fetch_sometime_data(coin_name, delta_days, data_type, from_date=None):
    now = datetime.datetime.now()
    if from_date is None:
        from_date = now - datetime.timedelta(days=delta_days)
    last_time = from_date
    i=0
    while True:
        i=i+1
        print("data type", data_type, i, datetime.datetime.now())
        if last_time > now:
            return
        start_time = last_time 
        end_time, url = make_date(start_time, delta_days, coin_name)
        print(url)

        prices = coinmarketcap.catch_data(SITE, coin_name, url, data_type)
        last_time = end_time
        time.sleep(0.2)


def run_once():
    now = datetime.datetime.now()
    format_today = datetime.datetime(now.year, now.month, now.day, 0,0,0)
    # old_day = datetime.datetime.now() - datetime.timedelta(days=1) #6年前
    # old_day = datetime.datetime(2013,5,1,0,0,0)
    old_day = None
    #fetch_5min_data(old_day, 'bitcoin')
    # fetch_5min_data(old_day, 'bitcoin')
    fetch_sometime_data('bitcoin', 1, 5, from_date=old_day)
    # fetch_sometime_data('bitcoin', 7, 15, from_date=old_day)   #7天
    # fetch_sometime_data('bitcoin', 30, 60, from_date=old_day) #30天
    # fetch_sometime_data('bitcoin', 90, 120, from_date=old_day)  #3个月
    day_1year_ago = format_today - datetime.timedelta(days=365)
    print(format_today, day_1year_ago)
    # fetch_sometime_data('bitcoin', 365, 1440, from_date=day_1year_ago) #1年
    fetch_sometime_data('bitcoin', 365*4, 2880, from_date=old_day) #全部



if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_executor('processpool')
    scheduler.add_job(run_once, 'interval', seconds=300)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # scheduler.start()
        run_once()
    except (KeyboardInterrupt, SystemExit):
        pass



