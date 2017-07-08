#coding:utf-8 
# -*- coding: utf-8 -*-

'''
Created on 2016年6月17日

@author: sx
'''

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
from Thread1 import Thread
import time
import logging
import math
import random
import sys
from scrapyIps import parseIps
from nbconvert.postprocessors.serve import ProxyHandler
import numpy as np

#可从文件读取，但类别不多 list存储
searchData=[
                         'A61C1/08 and 手机',
                         'A61B5/0245 and 手机',
                         'A61B5/11 and 手机',
                         'H04M1/12 and 手机',
                         'H04N7/18 and 手机',
                         'A63F13/24 and 手机',
                         'A63F13/90 and 手机',
                         'H04M1/02 and 手机',
                         'G09B7/02 and 手机',
                         'F24D17/02 and 手机',
                         'F24D19/10 and 手机',
                         'H02J13/00 and 手机',
                         'H04M1/11 and 手机']
def getIP():
    
    ipdir=os.getcwd()+"\ip.txt"
    f=open(ipdir,'r')
    iplist=f.readlines()
    #for ip in iplist:
    #   print ip
    rand=random.randint(0,len(iplist)-1)
    while iplist[rand]==socket.gethostbyname(socket.gethostname()):
        rand=random.randint(0,len(iplist)-1)
    
    ipandport=iplist[rand]
    ipandport=ipandport.strip()
    f.close()
    return ipandport




# 日志打印管理
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

#多线程test使用
class testThread:
    # patent=patentSpyer()
    def __init__(self,patent):
        self.name="main"
        self.Threadcounter=3
        self.ts=[]
        #self.methods={}
        self.pa=patent
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
            try:
                self.pa.getEncodeParams(cur+ThreadId*part)
            except:
                print "func：当前请求下载页面出错，继续别的页面"
                continue
       
    def spare(self,start,end):
        thread = threading.current_thread()
        logging.debug ("Thread:"+thread.getName())
      
        for i in range(start,end):
            try:
                self.pa.getEncodeParams(i) 
            except:
                print "spare：当前请求下载页面出错，继续别的页面"
                continue
    def stopThreads(self):
        for th in self.ts:
            if th.isAlive():
                print "线程未结束，结束当前线程"
                logging.debug("线程未结束，结束当前线程")
                th.terminate() 
                
    def threadFork(self):
        #ts = []
        #pages=self.pa.getPageNums()
        pages=self.pa.getPageNums()
        # 此处为 爬取的页码数 作为测试用10页，其中每页10相
        #pages=20
        parts=pages/self.Threadcounter        
        for currenthread in xrange(self.Threadcounter):
            try:
                th = Thread(target=self.func,args=(parts,currenthread),name="Thread"+str(currenthread))
                self.ts.append(th)
            except:
                print "不能创建线程" 
                continue
        sparestart=parts*self.Threadcounter+1
        if parts*self.Threadcounter<pages:
            try:
                th=Thread(target=self.spare,args=(sparestart,pages+1))
                self.ts.append(th)
            except:
                print "不能创建线程" 

        for th in self.ts:
            th.setDaemon(True)
            try:
                th.start()
            except:
                print "不能启动线程"
                continue
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

def setProxy(opener,proxy):
    flag=True
    while flag:
        try:
            #handler=ProxyHandler({"http":'http://%s/' % proxy}) 必须加 urllib2 ，否则直接异常 
            handler=urllib2.ProxyHandler({"http":proxy})
            opener.add_handler(handler)
            urllib2.install_opener(opener)
            #作为测试 代理可用否
            #urllib2.urlopen("http://www.baidu.com").read()
            
            flag=False
        except:
            proxy=getIP()    
    
    return opener

# 向服务器发送请求，处理异常 timeout socketerror 等，重发处理
def get(opener,req,retries=10):
    #请求太快，每次请求时sleep 2秒
    sec=np.random.normal(5,3)
    if sec<=0:
        sec=1
    
    time.sleep(sec)
    logging.info("send request")
    if retries<=0:
        logging.info("send request times over")
        return None 
    try:
        response = opener.open(req)
        data = response.read() 
    except URLError as e:
        if isinstance(e.reason, socket.timeout):
            logging.info("request timeout and rerequest")
            time.sleep(5)
            return get(opener,req,retries-1) 
        if hasattr(e,"reason"):
            logging.info("URLError,we fail to send to server")
            logging.debug("reason:")
            logging.debug(e.reason)
            time.sleep(5)
            return get(opener,req,retries-1) 
        elif hasattr(e,"code"):
            logging.info("the server cannot fulfill the req")
            logging.debug("error code:")
            time.sleep(5)
            logging.debug(e.code)
            return  get(opener,req,retries-1)  
    except socket.timeout:
        logging.debug("timeout,request again")
        time.sleep(5)
        return get(opener,req,retries-1)   
    except socket.error:
        logging.debug("socket.error: request again")
        time.sleep(5)
        return get(opener,req,retries-1) 
    logging.debug("get finally")
    #response.close()
    return data

# 判断页面是否异常，访问受限
def judgeContent(htmltext,opener,req):
    flag=True
    data=htmltext
    while flag:
        m = re.search(r"\<title\>[\s\S]*\</title\>",data)
        if m:
            t=m.group().strip("\<?/title>").strip()
            if t=="访问受限":
                print "ip访问受限，change proxy"
                proxy=getIP()
                opener=setProxy(opener, proxy)
                time.sleep(10)
                html=get(opener, req, 20)
                data=decodegzip(html)   
            elif t=="异常页面":
                print "异常页面，重新发送请求"
                time.sleep(10)    
                html=get(opener, req, 20)
                data=decodegzip(html) 
            else:
                flag=False 
        else:
            flag=False
    return data
# 解压缩 从服务器返回为压缩的，需要解压
def decodegzip(rawtext):   
    bi = io.BytesIO(rawtext)
    gf = gzip.GzipFile(fileobj=bi, mode="rb")
    textdecode=gf.read()
    return textdecode

#主要的spyder类，负责发送，返回，多次处理
class patentSpyer:
    def __init__(self,requestData='手机'):
        self.url="http://www.pss-system.gov.cn/sipopublicsearch/search/smartSearch-executeSmartSearch.shtml"
        #self.proxyURL=""
        # post data header 
        self.PatentClass=requestData
        self.Header={
        'Host':'www.pss-system.gov.cn',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
        'Referer':'http://www.pss-system.gov.cn/sipopublicsearch/search/searchHome-searchIndex.shtml?params=991CFE73D4DF553253D44E119219BF31366856FF4B152226CAE4DB031259396A',
        'Content-Type':'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Accept': 'text/html, */*',
        #'Content-Length': '132',#'140', 
        'Origin': 'http://www.pss-system.gov.cn',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8'
        }
       
        self.post={  
       
        #'searchCondition.searchExp':'手机',
        
        'searchCondition.searchExp':requestData,
        #可修改 实际应该为一个 变量 string 根据查询修改
        
        'searchCondition.dbId':'VDB',
        'searchCondition.searchType':'Sino_foreign',
        'wee.bizlog.modulelevel':'0200101'
        }
        self.parseFlag=True
        self.postParserData=None
        self.cookie = cookielib.CookieJar()  
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        
    """发送post请求，搜索：得到基本页面
    # the first send request (post) 
    #get the undecodegzip the content
    # params: opener,post ,url,header
    # return html(need to decodezip)  
    #返回为解码的页面源码
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
        html=get(opener, req, 20)
        #请求次数达到20次 ，返回none ，sleep 20秒，重复请求20次
        while html==None:
            logging.info("重复请求20次")
            time.sleep(20)
            html=get(opener, req, 20)
        #解码
        text=decodegzip(html)
        #判断是否返回异常页面
        judgeContent(text, opener, req)

            
        logging.debug("readHtml get the response")
         
        #打印返回的内容#
        
        return html
    """
    get the abract content need to post param,then the server encode param before it send to client.
    we use the param that encoded ,join the url end ,then send the server (get)
    #要得到简要信息，需要post param 我们需要，用服务器编码后的post param，加入url尾部，然后发送get请求 
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
        #'Content-Length': '129'
        
        }
        return Header   
    
    
    
    
    
    """
    pages 需要readhtml() parse after get the total of pages
    return pagenums :total pages
    #从readHtml（）得到页面，解析出总共的页码数
    """
    def getPageNums(self):
        logging.debug("parser function:get the nums of pages:")
        # 解析第一页得到总页数
        all_the_text=self.readHtml(self.opener,self.post,self.url,self.Header)
        
        all_the_text_decode=decodegzip(all_the_text)
        soup=BeautifulSoup(all_the_text_decode)
        logging.debug("get the html soup")
        #commandsearchnum 里面有总pages数
        #pages=10
        
        pages=soup.select("#commandSearchNum")[0]['value']
        
            
        logging.debug("found the pagesnums:")
        
        pagenums=int(pages)
        pagenums=pagenums/10
        logging.debug(pagenums)
        return pagenums
    
    """
    1.readHtml get params(首页),or parse(其他页面) get params
    2. post params get params and construct url+parmas  发送请求得到编码后的param
    3.send get request 发送get请求
    4.store in sql but now we first write into files 写入文件
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
            
    """
     1 解析 得到 nrdan id 构造post param ，然后发送出去，得到编码后的param
     2 发送get请求 得到简要信息页面
     3 写入文件 html源码
    """       
    def getEncoParamSendreq(self,currentpage,rawtext_decode):

        contextPath="http://www.pss-system.gov.cn/sipopublicsearch"
        #seconds=2
        logging.debug("html to soup")
        soup=BeautifulSoup(rawtext_decode)
        nrdAn=soup.findAll("input",attrs={"name":re.compile("^nrdAn")})# if match 解析；else 重复
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
            paramsDeal=get(opener, req, retries=20) 
            
            #请求次数达到20次 ，返回none ，sleep 20秒，重复请求20次
            while paramsDeal==None:
                logging.info("重复请求20次")
                timeout=timeout+10
                socket.setdefaulttimeout(timeout)
                time.sleep(20)
                paramsDeal=get(opener, req, 20)
            #解码
            text=decodegzip(paramsDeal)
                #判断是否返回异常页面
            text=judgeContent(text, opener, req)
            logging.debug("paramencod.shtml already return")
            #for ck in cookie:
            #   print type(ck)
            #   print ck 
            #decode the param (gzip need to zip)
            urlparam=text
            logging.debug(type(urlparam))
            urlparam=eval(urlparam)
            #concaten the url then send the request
            #之前手机请求的url ，现在需要更改的url
            #url = contextPath + "/search/showAbstractInfo-viewAbstractInfo.shtml?"+urlparam["params"]
            url = contextPath + "/search/showAbstractInfo-viewAbstractInfo_altered.shtml?"+urlparam["params"]
           
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
            rawcontent=get(opener, req, retries=20)
            
            #请求次数达到20次 ，返回none ，sleep 20秒，重复请求20次
            while rawcontent==None:
                logging.info("重复请求20次")
                time.sleep(20)
                rawcontent=get(opener, req, 20)
            #解码
            text=decodegzip(rawcontent)
                #判断是否返回异常页面
            text=judgeContent(text, opener, req)
            
            logging.debug("get return(response:showabstractInfo.shtml),read the html")
           
            contents=text
            #content_unparse=decodegzip(rawcontent)
            #print contents
            x=j#currentpage item 
            y=currentpage#page
            logging.debug("write file:")
            patCls=self.PatentClass.decode("utf-8")
            patclass=patCls
            if patCls.find('/'):
                patclass=patCls.replace('/','-')
            
            path="C:/Users/shixiong/Desktop/download/patent"+patclass
            if not os.path.isdir(path):
                os.mkdir(path)    
            f=open(path+"/page_"+str(y)+"item_"+str(x)+".txt",'w')
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
        des=descont[0].getText().strip()
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

    def getParserPostData(self):
        logging.debug(" parser function: readHtml start and parse:")
        # 解析第一页得到总页数和跳转页的请求参数，发送请求得到相应页面

        all_the_text=self.readHtml(self.opener,self.post,self.url,self.Header)
        logging.debug("parser function: readHtml end:")
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
        self.postParserData=postData
        #pagestart 代表下一页的start set resultpageination.start=pagestart  
        #pagestart each time +10
    """
    parser function: parse html to get the pages and post pagestart to get the content of \
    you request :pagestart represent the page
    parser 函数解析html 读取下一页  
    param:需要修改 增加参数 添加 0 10 20 ....30 作为页面开始, 当前函数默认值10为第二页resultlist
    return :请求的页面源码（已经解码过的）
    """        
    def parser(self,pagestart=10):
        if self.parseFlag==True:
            self.getParserPostData()
            self.parseFlag=False
        #pagestart=10
        postData=self.postParserData
        postData["resultPagination.start"]=str(pagestart)        
        logging.debug("the startpage %d of the htmls is: ",pagestart/10+1)
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
        logging.debug("parser function: send get:(req:showserchResult-startWa.shtml)")
        html2=get(self.opener, req, retries=10)
        
        #请求次数达到20次 ，返回none ，sleep 20秒，重复请求20次
        while html2==None:
            logging.info("重复请求20次")
            time.sleep(20)
            html2=get(self.opener, req, 20)
        #解码
        text=decodegzip(html2)
        #判断是否返回异常页面
        text=judgeContent(text, self.opener, req)
        
        logging.debug("parser function: send return (response:showsearchResult_startWa.shtml)")
        html2src=text
        
        #print "the src of page is:"
        #print html2src
        return html2src
 
if __name__=='__main__':
    logconfig()
    logging.info("the spyer start:")
    pa=patentSpyer(postData=searchData[1])
    
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
