#coding:utf-8
'''
Created on 2016年3月31日
在scrapy 加入了ip 代理
代理ip测试
@author: shixiong
'''
import logging
import scrapy331
import time
if __name__=="__main__":
    scrapy331.logconfig()
    logging.info("the spyer start:")
    
    searchItem=scrapy331.searchData
    # patentSpyer 增加了search 相
    for i in range(len(searchItem)):
        pa=scrapy331.patentSpyer(postData=searchItem[i])
        mythread=scrapy331.testThread(pa)
        mythread.threadRun()
        
