#coding:utf-8 
"""
Created on Thu Mar 10 09:30:53 2016

@author: shixiong
# -*- coding: utf-8 -*-
""
Spyder Editor
This is a temporary script file.
"""
import io
import gzip
import urllib
import urllib2
import cookielib
import codecs
import time,os
import re
from bs4 import BeautifulSoup
#from selenium import webdriver 
class patentSpyer:
    def __init__(self):
        self.url="http://www.pss-system.gov.cn/sipopublicsearch/search/smartSearch-executeSmartSearch.shtml"
        #self.proxyURL=""
# post data header        
        self.Header={
        'Host':'www.pss-system.gov.cn',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
        'Referer':'http://www.pss-system.gov.cn/sipopublicsearch/search/searchHome-searchIndex.shtml?params=991CFE73D4DF553253D44E119219BF31366856FF4B152226CAE4DB031259396A',
        'Content-Type':'application/x-www-form-urlencoded',
        'Connection':'keep-alive',
        'Accept': 'text/html, */*',
        'Origin': 'http://www.pss-system.gov.cn',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Encoding': 'gzip',
        'Accept-Language': 'zh-CN,zh;q=0.8'
        }
        self.post={  
       
        'searchCondition.searchExp':'手机',
#可修改 实际应该为一个 变量 string 根据查询修改
        
        'searchCondition.dbId':'VDB',
        'searchCondition.searchType':'Sino_foreign',
        'wee.bizlog.modulelevel':'0200101'
        }
        
        self.cookie = cookielib.CookieJar()  
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
       
    def readHtml(self,post,url):
        #需要POST的数据#
        postdata=urllib.urlencode(post)
        #自定义一个请求#
        req = urllib2.Request(  
            url = url,  
            data = postdata,
            headers = self.Header 
        )
        
        #访问该链接#
        
        result = self.opener.open(req)   
        
        html=result.read()
        #打印返回的内容#
        print result
        
        return html
    """
    params post request header
    """
    def paramHeader(self):
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
        cookie = cookielib.CookieJar()  
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    
        return opener   
    
    
    
    
    
    """
    pages 需要readhtml() parse after get the total of pages
      
    """
    def getEncodeParams(self,pages):
       
        contextPath="http://www.pss-system.gov.cn/sipopublicsearch"
        for i in range(pages):
            currentpage=i+1
            if currentpage==1:
                rawtext=self.readHtml(self.post,self.url)
                soup=BeautifulSoup(rawtext)
                nrdAn=soup.findAll("input",attrs={"name":re.compile("^nrdAn")})
                sid=soup.findAll("input",attrs={"name":re.compile("^idHidden")})
            
                for j in range(1):
                    params="nrdAn="+nrdAn[j]["value"]+"@==@cid="+sid[j]["value"]+"@==@sid="+sid[j]["value"]+"@==@wee.bizlog.modulelevel=0201101" 
                    url = contextPath + "/search/showAbstractInfo-viewAbstractInfo.shtml?"+params
                    urlpost=contextPath+"/portal/paramRewriter-paramEncode.shtml"
                    post={"params":params
                    }
                    postdata=urllib.urlencode(post)
                    #自定义一个请求#
                    req = urllib2.Request(  
                        url = urlpost,  
                        data = postdata
                    )
        
                    #访问该链接#
        
                    opener=self.paramHeader()
                    result = opener.open(req)   
                    paramsDeal=result.read()
            else:
                pagestart=currentpage*10-10
                rawtext=self.parser(pagestart)
                soup=BeautifulSoup(rawtext)
                nrdAn=soup.findAll("input",attrs={"name":re.compile("^nrdAn")})
                sid=soup.findAll("input",attrs={"name":re.compile("^idHidden")})
                """
                get the nrdan list and sid list 
                construct the params
                post the parms
                get encode paramas
                then use urllib get the abractcontent
                """
                for j in range(1):# range 10 each page has ten items
                    params="nrdAn="+nrdAn[j]["value"]+"@==@cid="+sid[j]["value"]+"@==@sid="+sid[j]["value"]+"@==@wee.bizlog.modulelevel=0201101" 
                    url = contextPath + "/search/showAbstractInfo-viewAbstractInfo.shtml?"+params
                    urlpost=contextPath+"/portal/paramRewriter-paramEncode.shtml"
                    post={"params":params
                    }
                    postdata=urllib.urlencode(post)
                    #自定义一个请求#
                    req = urllib2.Request(  
                        url = urlpost,  
                        data = postdata
                    )
                    opener=self.paramHeader()
                    #访问该链接#
                    result = opener.open(req)   
                    paramsDeal=result.read()


    """
    
    解析读取的页面：
    返回页面的信息：
    返回：
    des
    id
    title
    
    """
        
    def getAbContent(self):
        
        currentpage=0
        pages=1
        """pages 需要readhtml() parse after get the total of pages
        """
        contextPath="http://www.pss-system.gov.cn/sipopublicsearch"
        for i in range(pages):
            currentpage=i+1
            if currentpage==1:
                rawtext=self.readHtml(self.post,self.url)
                soup=BeautifulSoup(rawtext)
                nrdAn=soup.findAll("input",attrs={"name":re.compile("^nrdAn")})
                sid=soup.findAll("input",attrs={"name":re.compile("^idHidden")})
            
                for j in range(1):
                    params="nrdAn="+nrdAn[j]["value"]+"@==@cid="+sid[j]["value"]+"@==@sid="+sid[j]["value"]+"@==@wee.bizlog.modulelevel=0201101" 
                    url = contextPath + "/search/showAbstractInfo-viewAbstractInfo.shtml?"+params
                    urlpost=contextPath+"/portal/paramRewriter-paramEncode.shtml"
                    post={"params":params
                    }
                    postdata=urllib.urlencode(post)
                    #自定义一个请求#
                    req = urllib2.Request(  
                        url = urlpost,  
                        data = postdata
                    )
        
                    #访问该链接#
                    result = self.opener.open(req)   
                    paramsDeal=result.read()
        #return pid,title,des
        return paramsDeal


    
    """
    
    parser 函数解析html 读取下一页
      
    需要修改 增加参数 添加 0 10 20 ....30 作为页面开始
    当前函数固定10为第二页resultlist
    """        
    def parser(self,pagestart=10):
        all_the_text=self.readHtml(self.post,self.url)
        print "typeof (text):",type(all_the_text)
   
        
        print all_the_text.decode("utf-8")
        soup=BeautifulSoup(all_the_text)
        print "the html contents is:"
        print soup
        form=soup.select("#resultlistForm")
        print "the form is :",form
        contents= form[0].contents
        postData={}
        
        for i in range(len(contents)):
            print contents[i]['name'],contents[i]['value']
            postData[contents[i]['name']]=contents[i]['value']
            print " "
        postData["searchCondition.searchExp"]=postData["searchCondition.searchExp"].encode("utf-8")
#               pagestart 代表下一页的start set resultpageination.start=pagestart  
        #pagestart each time +10
        #pagestart=10
        
        postData["resultPagination.start"]=str(pagestart)        
        print postData
        nextpage='showSearchResult-startWa.shtml'
        nextpageurl= 'http://www.pss-system.gov.cn/sipopublicsearch/search/'+nextpage
        post=urllib.urlencode(postData)
        req=urllib2.Request(
            url=nextpageurl,
            data=post
        )
        result=self.opener.open(req)
        html2=result.read()
            
        return html2
if __name__=='__main__':
    print "the spyer start:"
    pa=patentSpyer()
    print "read function:"
    post=pa.post
    url=pa.url
    # read html 
    rawtext=pa.readHtml(post,url)
    # gzip decode get the content
    bi = io.BytesIO(rawtext)
    gf = gzip.GzipFile(fileobj=bi, mode="rb")
    textdecode=gf.read()
    print textdecode
    print "getAbcontent function:"
 #   param=pa.getEncodeParams(1)
    print "end getabcontent"
    #print "parse function:"
    #all_the_text=pa.parser()
    #print all_the_text 
    #print form
    #file_object = codecs.open('data2.txt', 'w','utf-8')
  #  print all_the_text
    #txt=unicode(all_the_text,"utf-8")
    #file_object.write(u'中文')
    #file_object.write(txt)
    
#   post 之后的url页面 
        
    
  #  file_object.close()
    print "the spyder end"
    
# 浏览器读取html find element 触发js函数
    
   