#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.websocket import websocket_connect


class Client(object):
    def __init__(self, url, timeout):
        self.url = url
        self.timeout = timeout
        self.ioloop = IOLoop.instance()
        self.ws = None
        self.clientId = 123
        self.connect()
        PeriodicCallback(self.keep_alive, 20000, io_loop=self.ioloop).start()
        self.ioloop.start()
        

    @gen.coroutine
    def connect(self):
        print("trying to connect")
        cid = self.clientId
        try:
            self.ws = yield websocket_connect(self.url, connect_timeout=30)
            
        except Exception as e:
            print("connection error")
        else:
            print("connected")
            self.ws.write_message('{"body": "", "cmd": "register", "from": "%s"}' % cid)
            self.run()

    @gen.coroutine
    def run(self):
        while True:
            msg = yield self.ws.read_message()
            if msg is None:
                print("connection closed")
                # self.ws = None
                self.ws.write_message('{"cmd": "keepalive"}')
                # break
                continue
            print(msg)
            parsed = tornado.escape.json_decode(msg)
            cmd = parsed["cmd"]
            if cmd == "message":
                self.ws.write_message('{"body": "ok", "from": "clientId", "cmd": "ack"}')

    def keep_alive(self):
        if self.ws is None:
            self.connect()
        else:
            self.ws.write_message('{"cmd": "keepalive"}')

if __name__ == "__main__":
    client = Client("ws://localhost:8888/chatsocket", 30)

