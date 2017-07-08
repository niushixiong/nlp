#coding:utf-8 
"""
Created on 3.28 15:30:16 2016

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
import socket
from bs4 import BeautifulSoup
from urllib2 import URLError
from urllib2 import HTTPError
import socket
import threading
import time
import logging
import math
import random
import sys
from scrapyIps import parseIps
def getIP():
    ipdir=os.getcwd()+"\ip.txt"
    f=open(ipdir,'r')
    iplist=f.readlines()
    #for ip in iplist:
     #   print ip
    rand=random.randint(0,len(iplist))
    while iplist[rand]==socket.gethostbyname(socket.gethostname()):
        rand=random.randint(0,len(iplist))
    
    ipandport=iplist[rand]
    ipandport=ipandport.strip()
    return ipandport





def logconfig():
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='scrapy.log',
                    filemode='w')
    
    #################################################################################################
    #定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    #################################################################################################


class testThread:
    def __init__(self):
        self.name="main"
        self.Threadcounter=5
        self.ts=[]
        #self.methods={}
        self.pa=patentSpyer()
    def threadRun(self):
        #name=threading.current_thread().getName()
        #print "curent thread name:"+name
        #print name+" thread run getEncodeParams("+str(currentpage)+")"
        self.threadFork()
        #print name+" thread end getEncodeParams("+str(currentpage)+")"
    
        
           
    def func(self,part,ThreadId):
        thread = threading.current_thread()
        logging.debug("Thread:"+thread.getName())
        for cur in range(1,part+1):
            self.pa.getEncodeParams(cur+ThreadId*part)
            
    def spare(self,start,end):
        thread = threading.current_thread()
        logging.debug ("Thread:"+thread.getName())
        for i in range(start,end):
            self.pa.getEncodeParams(i)    
    
    def threadFork(self):
        #ts = []
        #pages=self.pa.getPageNums()
        pages=self.pa.getPageNums()
        pages=100
        parts=pages/self.Threadcounter        
        for currenthread in xrange(self.Threadcounter):
            th = threading.Thread(target=self.func,args=(parts,currenthread),name="Thread"+str(currenthread))
            self.ts.append(th)
            
        sparestart=parts*self.Threadcounter+1
        if parts*self.Threadcounter<pages:
            th=threading.Thread(target=self.spare,args=(sparestart,pages+1))
            self.ts.append(th)
            
        for th in self.ts:
            th.setDaemon(True)
            th.start()
        th.join()
#from selenium import webdriver#模拟浏览器 

"""
#  gzip decode get the content
#  param：rawtext that need to dezip
#  return: textdecode which already decoded 
#
"""
timeout = 10
socket.setdefaulttimeout(timeout)
def get(opener,req,retries=10):
    logging.debug("send request(with try catch)")
    try:
        response = opener.open(req)
        data = response.read()    
    except URLError as e:
        if isinstance(e.reason, socket.timeout):
            logging.debug("request timeout and rerequest")
            time.sleep(2)
            return get(opener,req,retries-1)
        if hasattr(e,"reason"):
            logging.debug("URLError,we fail to send to server")
            logging.debug("reason:",e.reason)
            if retries>0:
                time.sleep(10)
                
                return get(opener,req,retries-1)
            else:
                logging.debug('10 times request Failed',req)
                return ''
        elif hasattr(e,"code"):
            logging.debug("the server cannot fulfill the req")
            logging.debug("error code:",e.code)
            if retries>0:
                time.sleep(60)
                if e.code==403:
                    return e.code
                return get(opener,req,retries-1)
            else:
                logging.debug('10 times request Failed',req)
                return ''
    except socket.timeout:
        logging.debug("timeout,request again")
        time.sleep(2)
        return get(opener,req,retries-1)   
    except socket.error:
        logging.debug("socket.error: request again")
        time.sleep(10)
        return get(opener, req, retries-1)
    logging.debug("get finally")
    return data




def decodegzip(rawtext):   
    bi = io.BytesIO(rawtext)
    gf = gzip.GzipFile(fileobj=bi, mode="rb")
    textdecode=gf.read()
    return textdecode



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
        
    """
    # the first send request (post) 
    #get the undecodegzip the content
    # params: opener,post ,url,header
    # return html(need to decodezip)  
    """
    def readHtml(self,opener,post,url,header):
        #需要POST的数据#
        postdata=urllib.urlencode(post)
        #自定义一个请求#
        req = urllib2.Request(  
            url = url,  
            data = postdata,
            headers = header 
        )
        
        #访问该链接#
        logging.debug("readHtml send req start")
        html=get(opener, req, 10)
        if html==403:
            ipport=getIP()
            proxy_support = urllib2.ProxyHandler({'http':ipport})
            opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
            urllib2.install_opener(opener)
            html = urllib2.urlopen('http://XXXX').read()
            
        logging.debug("readHtml get the response")
         
        #打印返回的内容#
        
        return html
    """
    get the abract content need to post param,then the server encode param before it send to client.
    we use the param that encoded ,join the url end ,then send the server (get)
     
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
        return Header   
    
    
    
    
    
    """
    pages 需要readhtml() parse after get the total of pages
    return pagenums :total pages
    """
    def getPageNums(self):
        logging.debug("parser function:get the nums of pages:")
        # 解析第一页得到总页数
        all_the_text=self.readHtml(self.opener,self.post,self.url,self.Header)
        all_the_text_decode=decodegzip(all_the_text)
        soup=BeautifulSoup(all_the_text_decode)
        logging.debug("get the html soup")
        #commandsearchnum 里面有总pages数
      
        pages=soup.select("#commandSearchNum")[0]['value']
        logging.debug("found the pagesnums:")
        logging.debug(pages)
        pagenums=int(pages)
        return pagenums
    
    """
    1.readHtml get params(首页),or parse(其他页面) get params
    2. post params get params and construct url+parmas 
    3.send get request
    4.store in sql but now we first write into files
    """
    def getEncodeParams(self,currentpage=1):# the function name need to change ,
        #and need to update to 
        #1.increase the deparser the content 
        #2.and save it to sqllite
            
        #search first page
        
        if currentpage==1:
            logging.debug("readHtml function start:")
            rawtext=self.readHtml(self.opener,self.post,self.url,self.Header)
            logging.debug("readHtml end")
            rawtext_decode=decodegzip(rawtext)
            logging.debug("getEncoParamSendreq function start:")
            self.getEncoParamSendreq(currentpage,rawtext_decode)
            logging.debug("getEncoParamSendreq function end")
        else:
            pagestart=currentpage*10-10
            logging.debug("parser function start")
            rawtext_decode=self.parser(pagestart)
            logging.debug("parser function end")
            #rawtext_decode=decodegzip(rawtext)
            logging.debug("getEncoParamSendreq function start:")
            self.getEncoParamSendreq(currentpage,rawtext_decode)
            logging.debug("getEncoParamSendreq function end")
            
            
    def getEncoParamSendreq(self,currentpage,rawtext_decode):

        contextPath="http://www.pss-system.gov.cn/sipopublicsearch"
        #seconds=2
        logging.debug("html to soup")
        soup=BeautifulSoup(rawtext_decode)
        nrdAn=soup.findAll("input",attrs={"name":re.compile("^nrdAn")})
        sid=soup.findAll("input",attrs={"name":re.compile("^idHidden")})
        """
        get the nrdan list and sid list 
        construct the params
        post the parms
        get encode paramas
        then use urllib get the abractcontent
        """ 
        logging.debug("start to page"+str(currentpage)+" get each item(10)")
        for j in range(0,10):# range 10 each page has ten items
            params="nrdAn="+nrdAn[j]["value"]+"@==@cid="+sid[j]["value"]+"@==@sid="+sid[j]["value"]+"@==@wee.bizlog.modulelevel=0201101" 
    
            urlpost=contextPath+"/portal/paramRewriter-paramEncode.shtml"
            post={"params":params
            }
            postdata=urllib.urlencode(post)
            #自定义一个请求#
            req = urllib2.Request(  
                url = urlpost,  
                data = postdata,
                headers=self.paramHeader()
            )
    
            cookie = cookielib.CookieJar()  
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
            urllib2.install_opener(opener)
            #访问该链接#
            logging.debug("send the param to server(to get the paramDeal that server dealed)")
            #原来是result = urllib2.urlopen(req)
            paramsDeal=get(opener, req, retries=10) 
            logging.debug("paramencod.shtml already return")
            #for ck in cookie:
            #   print type(ck)
            #   print ck 
            #decode the param (gzip need to zip)
            urlparam=decodegzip(paramsDeal)
            logging.debug(type(urlparam))
            urlparam=eval(urlparam)
            #concaten the url then send the request
            url = contextPath + "/search/showAbstractInfo-viewAbstractInfo.shtml?"+urlparam["params"]
            logging.debug("send request to server:(req:showabstractInfo.shtml)")
            req=urllib2.Request(
                url=url,
                headers={
                        'Host':'www.pss-system.gov.cn',
                        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
                        'Referer':'http://www.pss-system.gov.cn/sipopublicsearch/search/search/showViewList.shtml',
                        'Connection':'keep-alive',
                        'Origin': 'http://www.pss-system.gov.cn',
                        'Accept-Encoding': 'gzip',
                        'Accept-Language': 'zh-CN,zh;q=0.8',
                        
                         }            )
            cookiestring=''
            for ck in self.cookie:
                cookiestring=cookiestring+ck.name+'='+ck.value+';'
            req.add_header("Cookie",cookiestring[0:-1])
            
            #html=urllib2.urlopen(req)
            
            #原来是html=urllib2.urlopen(req)
            rawcontent=get(opener, req, retries=10)
            
            logging.debug("get return(response:showabstractInfo.shtml),read the html")
           
            contents=decodegzip(rawcontent)
            #content_unparse=decodegzip(rawcontent)
            #print contents
            x=j#currentpage item 
            y=currentpage+1#page
            logging.debug("write file:")
            f=open("C:/Users/shixiong/Desktop/download/patent"+str(y)+"_"+str(x)+".txt",'w')
            f.write(contents)
            logging.debug("write file end")
            f.close()
            #time.sleep(seconds)


    """
    
        解析读取的页面：
        返回页面的信息：
        返回：
    dicts：（key ,value）对 
    for d,x in dicts.items():
        print "key:"+d+",value:"+x
    """
        
    def getAbContent(self,content):
        soup=BeautifulSoup(content)
        descont=soup.select(".content")
        # 摘要简介
        des=descont[0].string.strip()
        # 其他信息    
        divcont=soup.select("#abstractItemList")
        trs=divcont[0].findAll("tr",recursive=True)
        tds=divcont[0].findAll("td",recursive=True)
        tdkey=[]
        tdvalue=[]
        for i in range(len(trs)):
            tdcont=trs[i].contents
            #for t in range(len(tdcont)):
            #    str=tdcont[t].string.strip()
            #    print str,t
            tdkey.append(tdcont[1].string.strip())
            tdvalue.append(tdcont[3].string.strip())
        #转换为字典类型，key,value对
        dicts={}
        for i in range(len(tdkey)):
            logging.debug(tdkey[i])
            logging.debug(tdvalue[i])
            dicts[tdkey[i]]=tdvalue[i]
        
        # 标题
        titlecont=soup.select(".fmbt")
        title=titlecont[0].string.strip()
        dicts[u'发明名称']=title
        dicts[u'摘要']=des
        # dicts 里面所有类型统一为unicode类型
        for d,x in dicts.items():
            logging.debug(type(d),type(x))
            if type(d)=="str":
                d=d.decode("utf-8")
            if type(x)=="str":
                x=x.decode("utf-8")
            logging.debug("key:"+d+",value:"+x)
        
        return dicts

    
    """
    parser function: parse html to get the pages and post pagestart to get the content of \
    you request :pagestart represent the page
    parser 函数解析html 读取下一页  
    param:需要修改 增加参数 添加 0 10 20 ....30 作为页面开始, 当前函数默认值10为第二页resultlist
    return :请求的页面源码（已经解码过的）
    """        
    def parser(self,pagestart=10):
        logging.debug(" parse: readHtml start and parse:")
        # 解析第一页得到总页数和跳转页的请求参数，发送请求得到相应页面

        all_the_text=self.readHtml(self.opener,self.post,self.url,self.Header)
        logging.debug("parse: readHtml end:")
        all_the_text_decode=decodegzip(all_the_text)
        logging.debug("the html to  soup")
        soup=BeautifulSoup(all_the_text_decode)
        
        #form里面有post的name value ，commandsearchnum 里面有总pages数
        form=soup.select("#resultlistForm")
        # print "the form is :",form
        """get the post data"""
        logging.debug("form got and start to parse and construct the postData:") 
        contents= form[0].contents
        postData={}  
        for i in range(len(contents)):
            #print contents[i]['name'],contents[i]['value']
            postData[contents[i]['name']]=contents[i]['value']
            #print " "
        postData["searchCondition.searchExp"]=postData["searchCondition.searchExp"].encode("utf-8")
        #pagestart 代表下一页的start set resultpageination.start=pagestart  
        #pagestart each time +10
        #pagestart=10
        
        postData["resultPagination.start"]=str(pagestart)        
        logging.debug("the startpage %d of the htmls is: ",pagestart)
        logging.debug("postdata is:")
        logging.debug(postData)
        nextpage='showSearchResult-startWa.shtml'
        nextpageurl= 'http://www.pss-system.gov.cn/sipopublicsearch/search/'+nextpage
        post=urllib.urlencode(postData)
        req=urllib2.Request(
            url=nextpageurl,
            data=post
        )
        
        #原来是result=self.opener.open(req,timeout=)
        logging.debug("parse: send get:(req:showserchResult-startWa.shtml)")
        html2=get(self.opener, req, retries=10)
        logging.debug("parse: send return (response:showsearchResult_startWa.shtml)")
        html2src=decodegzip(html2)
        
        #print "the src of page is:"
        #print html2src
        return html2src
if __name__=='__main__':
    logconfig()
    logging.info("the spyer start:")
    pa=patentSpyer()
    
    """
    ######test the readHtml method #########
    print "read function:"
    post=pa.post
    url=pa.url
    # test read html method
    #rawtext=pa.readHtml(pa.opener,post,url,pa.Header)
    # gzip decode get the content
    bi = io.BytesIO(rawtext)
    gf = gzip.GzipFile(fileobj=bi, mode="rb")
    textdecode=gf.read()
    print textdecode
    """
    
    """  test getencodeparam function : page 3"""
    
    
    #print "getEncodeParams start"
    #pa.getEncodeParams(3)
    #for i in range(1,10):
    #    print "getEncodeParams start"
    #   pa.getEncodeParams(i)
    #getAbcontent function:in test.py pass 
    #print "end getabcontent"
    
   
    """ 
    ###  test the parse function ####
    print "parse function:"
    all_the_text=pa.parser()
    print "parse return"
    print "*************************************************************************"
    
    # gzip decode get the content
    file_object = codecs.open('data2.txt', 'w','utf-8')
    txt=unicode(all_the_text,"utf-8")
    file_object.write(txt)
    file_object.close()
    print "end the parse function"
    """
    
    """test multiply threads"""
    """
    mythread=testThread()
    mythread.threadRun()
    """
    pagenames=pa.getPageNums()
    print pagenames
    logging.info("the spyder end")
    
    # 浏览器读取html find element 触发js函数
    

#proxy_support = urllib2.ProxyHandler({'http':'http://XX.XX.XX.XX:XXXX'})
#opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
#urllib2.install_opener(opener)
#content = urllib2.urlopen('http://XXXX').read()