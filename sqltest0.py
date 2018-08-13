# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import os
import json

from easyspider.db import SpiderResult,SpiderTask, Session
from easyspider.utils import md5str


results = SpiderResult.query.filter(SpiderResult.id == 10851).all()

#print(results.content)
db = Session()
for res in results:
    print(res.id)
    jsons = json.loads(res.content)
    ctn = jsons['content']
    print(ctn)

    # urls = []
    # for ctn in contents:
    #     print(ctn['url'], ctn['content'])
    #     url = ctn['url']
    #     task = SpiderTask()
    #     task.project = 'juejin'
    #     task.task_id = md5str(url)
    #     task.url = url
    #     task.callback = 'on_entry_page'
    #     task.priority = 1
    #     task.last_time = 0
    #     task.status = 0
    #     task.result = json.dumps(ctn)
    #     db.add(task)
    #     db.commit()
                #print("%s\t\t%s\t%s\t%s" % (tag['title'], tag['viewsCount'], tag['subscribersCount'], tag['objectId']))

    #print(urls)
