# -*- coding: utf-8 -*-
#!/usr/bin/env python
import re
from easyspider.spider import EasySpider
from easyspider.cron import every, config
import json
from readability import Document

class Spider(EasySpider):

    @every(crontab=["*/30 * * * *"])
    def on_start(self):
        #url = "https://api.leancloud.cn/1.1/classes/Entry?&where=%7B%22tagsTitleArray%22%3A%7B%22%24in%22%3A%5B%22Docker%22%5D%7D%7D&include=user&limit=20&skip=20&order=-rankIndex"
        url = "https://api.leancloud.cn/1.1/classes/Tag?&where=%7B%7D&limit=500&order=-createdAt"
        self.fetch(url, callback=self.on_index_page)

    #age: minute
    @config(age=30*60) #age:30minute
    def on_index_page(self, response):
        print("response type", type(response.content.decode('utf-8')));
        resjson = json.loads(response.content.decode('utf-8'))
        print("resjson:", resjson)
        return resjson
        #for each in response.doc('a[href^="http://www.juejin.com"]').items():
        #    self.fetch(each.attr.href, callback=self.on_detail_page)

    @config(age=60*24*7, priority=9) #age:7days
    def on_detail_page(self, response):
        return {"title": response.doc('h1').text()}


    def on_entry_page(self, response):
        ctn = response.content
        doc = Document(ctn)
        return {'content': doc.summary()}
