#coding:utf-8
"""
Created on Thu Mar 17 14:40:34 2016

@author: sx
"""
from scrapy import patentSpyer
import sys
import urllib
import io
import gzip
import urllib2
import cookielib
import chardet
import re
from bs4 import BeautifulSoup

#from selenium import webdriver
def paramHeader():
        Header={
        'Host':'www.pss-system.gov.cn',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
        'Referer':'http://www.pss-system.gov.cn/sipopublicsearch/search/search/showViewList.shtml',
        'Content-Type':'application/x-www-form-urlencoded',
        'Connection':'keep-alive',
        'Accept': 'application/json, text/javascript, */*',
        'Origin': 'http://www.pss-system.gov.cn',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Content-Length': '129'
        
        }
        
        return Header 
if __name__=='__main__':
    print "the spyer start:"
    pa=patentSpyer()
    print "read function:"
    post=pa.post
    url=pa.url
    contextPath="http://www.pss-system.gov.cn/sipopublicsearch"
    rawtext=pa.readHtml(post,url)
    
    # gzip decode get the content
    bi = io.BytesIO(rawtext)
    gf = gzip.GzipFile(fileobj=bi, mode="rb")
    textdecode=gf.read()
    coding=chardet.detect(textdecode)
    if coding["encoding"]=="utf-8" or coding["encoding"]=="UTF-8":
        print textdecode
        content=textdecode
        f=open("C:/Users/shixiong/Desktop/niu.txt",'w')
        f.write(content)
        f.close()
    else:
        print "----------------------------------------------------"
        textgbkdecode=textdecode.decode('gbk')
        print textgbkdecode
        print "****************************************************"
        content=textgbkdecode.encode("utf-8")
        f=open("C:/Users/shixiong/Desktop/niu.txt",'w')
        f.write(content)
        f.close()
    soup=BeautifulSoup(content)
    nrdAn=soup.findAll("input",attrs={"name":re.compile("^nrdAn")})
    sid=soup.findAll("input",attrs={"name":re.compile("^idHidden")})
    # send post param get the encode param by server   
        
    for j in range(1):
        params="nrdAn="+nrdAn[j]["value"]+"@==@cid="+sid[j]["value"]+"@==@sid="+sid[j]["value"]+"@==@wee.bizlog.modulelevel=0201101" 
        url = contextPath + "/search/showAbstractInfo-viewAbstractInfo.shtml?"+params
        urlpost=contextPath+"/portal/paramRewriter-paramEncode.shtml"
        post={"params":params
        }
        cookie = cookielib.CookieJar()  
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        
        postdata=urllib.urlencode(post)
        #自定义一个请求#
        req = urllib2.Request(  
        url = urlpost,  
        data = postdata,
        headers=paramHeader()
        )
            
        #访问该链接#
            
        result = opener.open(req)   
        paramsDeal=result.read()
        