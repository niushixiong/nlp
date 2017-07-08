#coding:utf-8
'''
Created on 2016年3月31日

@author: sx
'''
import scrapy328

def f(a,b,c):
    x=y=0
    for i in range(c):
        x=x+a+y
        y=y+b
    return x
    


if __name__=="__main__":
    print f(-5,2,10)
    ip=scrapy328.getIP()
    print ip
    print "end"
