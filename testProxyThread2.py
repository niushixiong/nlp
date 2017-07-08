#coding:utf-8
'''
Created on 2016年6月17日

@author: sx
'''

import logging
from scrapy617 import patentSpyer
from scrapy617 import testThread
from scrapy617 import logconfig
from scrapy617 import searchData
import time
if __name__=="__main__":
    logconfig()
    logging.info("the spyer start:")
    
    #searchItem=['手机 and 处理器',
    #           '手机  and 显示器',
    #          '手机  and 摄像头',
    #         '手机 and 软件',
    #        '手机 and 电池']
    searchItem=["飞机 and B23","飞机 and B64","飞机 and B25","飞机 and A47"]
    # patentSpyer 增加了search 相
    for i in range(0,4):
        print "start:"
        try:
            pa=patentSpyer(searchItem[i])
            mythreads=testThread(pa)
            mythreads.threadRun()
        except:
            print "except：next请求项开始"
            continue
        mythreads.stopThreads()
        print "next 请求项开始"
        
