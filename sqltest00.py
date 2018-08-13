# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import os
import json

import requests

from readability import Document
from easyspider.db import SpiderResult,SpiderTask, Session

import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from easyspider.db.mysql import Session, ScopedSession

class BaseClass(object):
    query =  ScopedSession.query_property()
    def commit(self):
        db = ScopedSession()
        db.add(self)
        db.commit()

Base = declarative_base(cls=BaseClass)

class PostTopic(Base):
    __tablename__ = 'wec_topic'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    view_count = Column(Integer)
    uuid = Column(String)
    url = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())
    # query =  ScopedSession.query_property()

"""
DROP TABLE IF EXISTS `wec_topic`;
CREATE TABLE `wec_topic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `uuid` varchar(32) NOT NULL,
  `url` varchar(1000) NOT NULL,
  `view_count` int default 0,
  `content` MEDIUMTEXT,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_task_id` (`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

"""

db = Session()

tasks = SpiderTask.query.filter_by(status=200, callback='on_entry_page').all()
for task in tasks:
    res = SpiderResult.query.filter_by(task_id=task.task_id).one()
    if res is None:
        print("Error, not found result %s" % task.task_id)
        # continue
    if task.result:
        print("save res %s" % task.task_id)
        resjson = json.loads(task.result)
        cnt = resjson['collectionCount']
        title = resjson['title']
        content = json.loads(res.content)
        task_id = res.task_id
        post = PostTopic()
        post.uuid = task_id
        post.title = title
        post.content = content['content']
        post.url = resjson['originalUrl']
        db.add(post)
        db.commit()
    else:
        print("task result is null, %s" % res.task_id)
