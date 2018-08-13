# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import os
import json

from easyspider.db import SpiderResult,SpiderTask, Session
from easyspider.utils import md5str
results = SpiderResult.query.filter_by(id=7569).one()

print(results.content)

jsons = json.loads(results.content)
tags = jsons['results']

urls = []
for tag in tags:
    cnt = int(tag['subscribersCount'])
    fmt = """https://api.leancloud.cn/1.1/classes/Entry?&where={"tagsTitleArray":{"$in":["%s"]}}&include=user&limit=%d&skip=%d&order=-rankIndex"""
    total = int(tag['entriesCount'])
    i = 0

    while(i < total):
        print(fmt % (tag['title'], 20, i))
        urls.append(fmt % (tag['title'], 20, i))
        i += 20
            #print("%s\t\t%s\t%s\t%s" % (tag['title'], tag['viewsCount'], tag['subscribersCount'], tag['objectId']))

#print(urls)
db = Session()
for url in urls:
    task = SpiderTask()
    task.project = 'juejin'
    task.task_id = md5str(url)
    task.url = url
    task.callback = 'on_index_page'
    task.priority = 0
    task.last_time = 0
    task.status = 0
    db.add(task)
    db.commit()
    #task.create_at = now()
    print(url)
