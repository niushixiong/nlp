# -*- coding: utf-8 -*-
'''
Created on 2016年6月6日

@author: sx
'''
import urllib2
import urllib
import cookielib
import  io
import gzip
from nbconvert.postprocessors.serve import ProxyHandler
def decodegzip(rawtext):   
    bi = io.BytesIO(rawtext)
    gf = gzip.GzipFile(fileobj=bi, mode="rb")
    textdecode=gf.read()
    return textdecode
url="http://www.pss-system.gov.cn/sipopublicsearch/search/smartSearch-executeSmartSearch.shtml"
        #self.proxyURL=""
# post data header 

Header={
        'Host':'www.pss-system.gov.cn',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
        'Referer':'http://www.pss-system.gov.cn/sipopublicsearch/search/searchHome-searchIndex.shtml?params=991CFE73D4DF553253D44E119219BF31366856FF4B152226CAE4DB031259396A',
        'Content-Type':'application/x-www-form-urlencoded',
        'Connection':'keep-alive',
        'Accept': 'text/html, */*',
        'Content-Length': '140',
        'Origin': 'http://www.pss-system.gov.cn',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8'
        }
       
post={  
       
        #'searchCondition.searchExp':'手机',
        
        'searchCondition.searchExp':"电子书",
        #可修改 实际应该为一个 变量 string 根据查询修改
        
        'searchCondition.dbId':'VDB',
        'searchCondition.searchType':'Sino_foreign',
        'wee.bizlog.modulelevel':'0200101'
        }
        
proxy="1.69.36.97:8888"
#urllib2.ProxyHandler({'http': 'http://%s/' % proxy})
handler=urllib2.ProxyHandler({"http":proxy})
cookie = cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
opener.add_handler(handler)
urllib2.install_opener(opener)
postdata=urllib.urlencode(post)
        #自定义一个请求#
req = urllib2.Request(  
            url = url,  
            data = postdata,
            headers = Header 
        )
response = opener.open(req)
rawdata=response.read() 
html=decodegzip(rawdata)
print html
