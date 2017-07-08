#coding:utf-8
'''
Created on 2016年3月31日
在scrapy 加入了ip 代理
代理ip测试
@author: shixiong
'''
import logging
from scrapy617 import patentSpyer
from scrapy617 import testThread
from scrapy617 import logconfig
from scrapy617 import searchData
import numpy as np
import time
if __name__=="__main__":
    logconfig()
    logging.info("the spyer start:")
    searchItem=["飞机 and B64C1","飞机 and B64C25","飞机 and B64D11","飞机 and B64F5","飞机 and G06F17","飞机 and G01M9","飞机 and G05B17","飞机 and B60N2","飞机 and B60F5"]
    #searchItem=['手机 and 处理器',
                #'手机  and 显示器',
                #'手机  and 摄像头',
                #'手机 and 软件',
                #'手机 and 电池']
    
        #postData='手机'
    #for i in range(5):
        #print i
    #print searchItem[0],type(searchItem[0]),postData,type(postData)
    #print postData.decode("utf-8")
    print searchItem[0].decode("utf-8")
    counter=0
    # patentSpyer 增加了search 相
    for i in range(4,8):
        pa=patentSpyer(searchItem[i])
        num=pa.getPageNums()
        
        #if num>100:
        #    num=100
        
            
        for j in range(0,num):
            counter=counter+1
            try:
                pa.getEncodeParams(j) 
            except:
                print "func：当前请求下载页面出错，继续别的页面"
                continue
            sec=np.random.normal(8,4)
            if sec<=0:
                sec=2
            time.sleep(sec)
