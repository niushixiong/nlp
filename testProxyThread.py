#coding:utf-8
'''
Created on 2016年3月31日
在scrapy 加入了ip 代理
代理ip测试
@author: shixiong
'''
import logging
from scrapy331 import patentSpyer
from scrapy331 import testThread
from scrapy331 import logconfig
from scrapy331 import searchData
import time
if __name__=="__main__":
    logconfig()
    logging.info("the spyer start:")
    
    #searchItem=['手机 and 处理器',
     #           '手机  and 显示器',
      #          '手机  and 摄像头',
       #         '手机 and 软件',
        #        '手机 and 电池']
    searchItem=searchData
    # patentSpyer 增加了search 相
    for i in range(7,10):
        print "start:"
        pa=patentSpyer(postData=searchItem[i])
        mythread=testThread(pa)
        mythread.threadRun()
        print "threadRun"
        
