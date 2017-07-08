#coding=utf-8
'''
Created on 2016年3月25日
多线程
使用testDemo
demo 多线程测试成功后 ，在scrapy 实现
@author: sx
'''

import threading
import time


class testThread:
    def __init__(self):
        self.opener="selfopener"
        self.counter=1
    def test(self,p):
        time.sleep(0.001)
        name=threading.current_thread().getName()
        
        opener="test"+str(p)+"opener"
        time.sleep(2)
        print str(p)+"name:",name
        time.sleep(1)
        print str(p)+"selfopener:"+self.opener
        time.sleep(3)
        print str(p)+"testOpener:"+opener


ts = []
tethread=testThread()
for i in xrange(0,15):
    th = threading.Thread(target=tethread.test,args=[i])
    th.start()
    ts.append(th)


for i in ts:
    i.join()

print "hoho,end!!!!!"